#!/usr/bin/env python3
"""
Smart incremental ingestion script
Only processes new or modified files based on modification time tracking
"""

import os, sys, yaml, frontmatter, time, json, hashlib
from pathlib import Path
from tqdm import tqdm

from llama_index.core import (
    Settings, Document, VectorStoreIndex, StorageContext
)
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.readers import SimpleDirectoryReader

# ---- load config
CFG = yaml.safe_load(open("config.yaml"))
VAULT = Path(CFG["vault_path"])
COLL = CFG["collection_name"]
QDRANT_URL = CFG["qdrant_url"]

# Track processed files
BRAIN_DIR = Path("./brain")
BRAIN_DIR.mkdir(exist_ok=True)
TRACKING_FILE = BRAIN_DIR / "processed_files.json"

# ---- models
Settings.embed_model = OllamaEmbedding(
    model_name=CFG["embed_model"], 
    base_url="http://localhost:11434",
    embed_batch_size=1,
)
Settings.llm = Ollama(model=CFG["chat_model"], base_url="http://localhost:11434")

# ---- text splitter
splitter = SentenceSplitter(
    chunk_size=CFG["chunk_size"],
    chunk_overlap=CFG["chunk_overlap"],
)

# ---- helpers
def load_tracking_data():
    """Load tracking data of processed files"""
    if TRACKING_FILE.exists():
        try:
            with open(TRACKING_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_tracking_data(data):
    """Save tracking data"""
    with open(TRACKING_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def get_file_signature(fp: Path):
    """Get a signature for a file (mtime + size)"""
    stat = fp.stat()
    return f"{int(stat.st_mtime)}_{stat.st_size}"

def check_ollama():
    """Verify Ollama is running and embedding model is available."""
    try:
        import requests
        health = requests.get("http://localhost:11434/api/tags", timeout=5)
        if health.status_code != 200:
            return False
        
        models = health.json().get("models", [])
        embed_model_name = CFG["embed_model"].split(":")[0]
        model_available = any(embed_model_name in m.get("name", "") for m in models)
        
        if not model_available:
            print(f"\n⚠️  Warning: Embedding model '{CFG['embed_model']}' may not be available.")
            print(f"   Run: ollama pull {CFG['embed_model']}")
        
        return True
    except Exception as e:
        print(f"\n❌ Error checking Ollama: {e}", file=sys.stderr)
        return False

def read_markdown_with_frontmatter(fp: Path):
    post = frontmatter.load(fp)
    content = post.content
    meta = {k: post.get(k) for k in CFG["frontmatter_keys"] if k in post}
    return content, meta

def load_docs_incremental(vault: Path, tracking_data):
    """Load only new or modified documents"""
    md_files, other_files = [], []
    
    for p in vault.rglob("*"):
        if p.is_file() and not p.name.startswith('.'):
            if p.suffix.lower() in [".md", ".markdown"]:
                md_files.append(p)
            elif p.suffix.lower() in [".pdf", ".txt"]:
                other_files.append(p)
    
    docs = []
    new_files = []
    modified_files = []
    
    # Process markdown files
    for fp in md_files:
        file_key = str(fp)
        current_sig = get_file_signature(fp)
        
        if file_key not in tracking_data or tracking_data[file_key] != current_sig:
            text, meta = read_markdown_with_frontmatter(fp)
            meta.update({
                "source_path": str(fp),
                "ext": fp.suffix.lower(),
                "mod_time": int(fp.stat().st_mtime),
            })
            docs.append(Document(text=text, metadata=meta))
            
            if file_key in tracking_data:
                modified_files.append(fp.name)
            else:
                new_files.append(fp.name)
    
    # Process other files
    new_other = []
    for p in other_files:
        file_key = str(p)
        current_sig = get_file_signature(p)
        
        if file_key not in tracking_data or tracking_data[file_key] != current_sig:
            new_other.append(p)
            if file_key in tracking_data:
                modified_files.append(p.name)
            else:
                new_files.append(p.name)
    
    if new_other:
        reader = SimpleDirectoryReader(
            input_files=[str(p) for p in new_other],
            recursive=False,
        )
        for d in reader.load_data():
            md = dict(d.metadata or {})
            md.update({"source_path": md.get("file_path", md.get("source", ""))})
            d.metadata = md
            docs.append(d)
    
    return docs, new_files, modified_files

def main():
    if not VAULT.exists():
        print(f"Vault path {VAULT} not found. Create it and add files.", file=sys.stderr)
        sys.exit(1)

    # Check Ollama before starting
    print("==> Checking Ollama...")
    if not check_ollama():
        print("   ❌ Ollama is not responding or not available.", file=sys.stderr)
        print("   Please ensure Ollama is running: ollama serve", file=sys.stderr)
        sys.exit(1)
    print("   ✓ Ollama is ready")

    # Load tracking data
    print("==> Loading tracking data...")
    tracking_data = load_tracking_data()
    previously_processed = len(tracking_data)
    
    if previously_processed > 0:
        print(f"   Previously processed: {previously_processed} files")
    
    # Load only new/modified documents
    print("==> Scanning for new or modified documents...")
    docs, new_files, modified_files = load_docs_incremental(VAULT, tracking_data)
    
    if not docs:
        print("   ✓ No new or modified documents found. Everything is up to date!")
        sys.exit(0)
    
    print(f"   Found {len(docs)} documents to process:")
    if new_files:
        print(f"     • New: {len(new_files)} files")
    if modified_files:
        print(f"     • Modified: {len(modified_files)} files")

    # Split into nodes
    print("==> Splitting into chunks...")
    nodes = []
    file_signatures = {}
    
    for d in tqdm(docs, desc="Chunking"):
        source_path = d.metadata.get("source_path")
        if source_path:
            file_path = Path(source_path)
            if file_path.exists():
                file_signatures[str(file_path)] = get_file_signature(file_path)
        
        for n in splitter.get_nodes_from_documents([d]):
            nodes.append(n)
    
    print(f"   Created {len(nodes)} chunks from {len(docs)} documents")

    # Setup Qdrant
    print("==> Connecting Qdrant…")
    client = QdrantClient(url=QDRANT_URL)
    
    collections = client.get_collections().collections
    collection_exists = any(c.name == COLL for c in collections)
    
    vstore = QdrantVectorStore(client=client, collection_name=COLL)
    storage = StorageContext.from_defaults(vector_store=vstore)

    # Build / refresh index
    print(f"==> Indexing {len(nodes)} chunks...")
    
    # Test embedding endpoint before starting
    print("   Testing embedding endpoint...")
    try:
        test_embedding = Settings.embed_model.get_text_embedding("test")
        if not test_embedding or len(test_embedding) == 0:
            print("   ⚠️  Warning: Embedding test returned empty result")
        else:
            print(f"   ✓ Embedding endpoint working (vector size: {len(test_embedding)})")
    except Exception as e:
        print(f"   ❌ Embedding test failed: {e}", file=sys.stderr)
        print("   Please check Ollama and the embedding model", file=sys.stderr)
        sys.exit(1)
    
    # Load or create index
    try:
        index = VectorStoreIndex.from_vector_store(vstore)
        print("   Found existing index, adding new chunks...")
    except:
        index = VectorStoreIndex.from_documents([], storage_context=storage)
        print("   Creating new index...")
    
    # Process chunks with retry logic
    successful_chunks = 0
    failed_chunks = 0
    
    print("   Processing chunks (this may take a while)...")
    for i, node in enumerate(tqdm(nodes, desc="Indexing")):
        # Check Ollama periodically
        if i > 0 and i % 20 == 0:
            try:
                import requests
                health = requests.get("http://localhost:11434/api/tags", timeout=2)
                if health.status_code != 200:
                    print(f"\n   Warning: Ollama health check failed at chunk {i}")
            except:
                pass
        
        # Insert with retry
        success = False
        retries = 0
        while not success and retries < 2:
            try:
                index.insert_nodes([node])
                successful_chunks += 1
                success = True
            except Exception as e:
                retries += 1
                if retries < 2:
                    error_str = str(e)
                    if "EOF" in error_str or "500" in error_str:
                        time.sleep(3)
                        # Recreate connection
                        try:
                            Settings.embed_model = OllamaEmbedding(
                                model_name=CFG["embed_model"], 
                                base_url="http://localhost:11434",
                                embed_batch_size=1
                            )
                        except:
                            pass
                    else:
                        time.sleep(1)
                else:
                    failed_chunks += 1
                    print(f"\n   Failed to index chunk {i+1}: {str(e)[:100]}")
        
        # Delay between chunks
        time.sleep(0.5)
        
        # Longer pause every 10 chunks
        if (successful_chunks) % 10 == 0:
            time.sleep(2.0)
    
    # Update tracking data
    print("\n==> Updating tracking data...")
    tracking_data.update(file_signatures)
    save_tracking_data(tracking_data)
    
    # Summary
    print("\n" + "="*60)
    print(f"✓ Indexing complete!")
    print(f"  Successfully indexed: {successful_chunks} chunks")
    if failed_chunks > 0:
        print(f"  Failed: {failed_chunks} chunks")
    print(f"  Total tracked files: {len(tracking_data)}")
    print("="*60)
    
    if failed_chunks > 0:
        print("\nNote: Some chunks failed. You can re-run to retry failed documents.")

if __name__ == "__main__":
    main()

