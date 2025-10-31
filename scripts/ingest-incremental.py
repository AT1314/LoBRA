#!/usr/bin/env python3
"""
Incremental ingestion script for 8GB RAM systems
Processes documents one at a time to avoid memory issues
"""

import os, sys, yaml, frontmatter, time
from pathlib import Path
from tqdm import tqdm
import requests

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

# ---- helpers
def check_ollama(max_retries=5):
    """Check if Ollama is responding, restart if needed"""
    for i in range(max_retries):
        try:
            resp = requests.get("http://localhost:11434/api/tags", timeout=3)
            if resp.status_code == 200:
                return True
        except:
            pass
        
        if i < max_retries - 1:
            print(f"   Ollama not responding, waiting {2*(i+1)}s...")
            time.sleep(2 * (i + 1))
    
    print("ERROR: Ollama is not responding. Please restart:")
    print("  brew services restart ollama")
    return False

def read_markdown_with_frontmatter(fp: Path):
    post = frontmatter.load(fp)
    content = post.content
    meta = {k: post.get(k) for k in CFG["frontmatter_keys"] if k in post}
    return content, meta

def load_docs(vault: Path):
    md_files, other_files = [], []
    for p in vault.rglob("*"):
        if p.is_file():
            if p.suffix.lower() in [".md", ".markdown"]:
                md_files.append(p)
            else:
                other_files.append(p)

    docs = []
    
    for fp in md_files:
        text, meta = read_markdown_with_frontmatter(fp)
        meta.update({
            "source_path": str(fp),
            "ext": fp.suffix.lower(),
            "mod_time": int(fp.stat().st_mtime),
        })
        docs.append(Document(text=text, metadata=meta))

    if other_files:
        reader = SimpleDirectoryReader(
            input_files=[str(p) for p in other_files],
            recursive=False,
        )
        for d in reader.load_data():
            md = dict(d.metadata or {})
            md.update({"source_path": md.get("file_path", md.get("source", ""))})
            d.metadata = md
            docs.append(d)

    return docs

def process_document(document, index, splitter):
    """Process a single document and add to index"""
    # Split document into chunks
    nodes = splitter.get_nodes_from_documents([document])
    
    if not nodes:
        return 0, "No chunks created"
    
    # Process chunks one at a time
    successful = 0
    failed = 0
    
    for i, node in enumerate(nodes):
        # Check Ollama before each chunk
        if not check_ollama():
            return successful, f"Ollama not responding at chunk {i+1}"
        
        try:
            index.insert_nodes([node])
            successful += 1
            time.sleep(0.5)  # Delay between chunks
            
            # Extra pause every 5 chunks
            if (i + 1) % 5 == 0:
                time.sleep(1.0)
                
        except Exception as e:
            failed += 1
            error_msg = str(e)[:100]
            print(f"      Failed chunk {i+1}/{len(nodes)}: {error_msg}")
            
            # If Ollama crashed, wait longer
            if "EOF" in error_msg or "500" in error_msg:
                print(f"      Ollama may have crashed, waiting 5s...")
                time.sleep(5)
                if not check_ollama():
                    return successful, f"Ollama crashed at chunk {i+1}"
            
            # Skip failed chunks for now
            continue
    
    return successful, f"{successful} successful, {failed} failed"

def main():
    if not VAULT.exists():
        print(f"Vault path {VAULT} not found.", file=sys.stderr)
        sys.exit(1)

    # Check Ollama first
    print("==> Checking Ollama...")
    if not check_ollama():
        sys.exit(1)
    print("   ✓ Ollama is responding")

    # Setup models with minimal batching
    print("==> Setting up models...")
    Settings.embed_model = OllamaEmbedding(
        model_name=CFG["embed_model"], 
        base_url="http://localhost:11434",
        embed_batch_size=1,  # Process one at a time
    )
    Settings.llm = Ollama(model=CFG["chat_model"], base_url="http://localhost:11434")

    splitter = SentenceSplitter(
        chunk_size=CFG["chunk_size"],
        chunk_overlap=CFG["chunk_overlap"],
    )

    # Load documents
    print("==> Loading documents...")
    docs = load_docs(VAULT)
    if not docs:
        print("No documents found in vault/")
        sys.exit(0)
    
    print(f"   Found {len(docs)} documents")

    # Setup Qdrant
    print("==> Connecting Qdrant…")
    client = QdrantClient(url=QDRANT_URL)
    vstore = QdrantVectorStore(client=client, collection_name=COLL)
    storage = StorageContext.from_defaults(vector_store=vstore)

    # Try to load existing index
    try:
        index = VectorStoreIndex.from_vector_store(vstore)
        print("   Found existing index, will add to it...")
    except:
        index = VectorStoreIndex.from_documents([], storage_context=storage)
        print("   Creating new index...")

    # Process documents one at a time
    print(f"\n==> Processing {len(docs)} documents one at a time...")
    print("   (This will be slow but stable for 8GB RAM)\n")
    
    successful_docs = 0
    failed_docs = 0
    total_chunks = 0
    
    for i, doc in enumerate(docs, 1):
        doc_name = Path(doc.metadata.get("source_path", "unknown")).name
        print(f"[{i}/{len(docs)}] Processing: {doc_name}")
        
        # Check Ollama before each document
        if not check_ollama():
            print("   ✗ Stopping: Ollama not responding")
            break
        
        # Process document
        chunks_added, status = process_document(doc, index, splitter)
        
        if chunks_added > 0:
            successful_docs += 1
            total_chunks += chunks_added
            print(f"   ✓ Added {chunks_added} chunks - {status}")
        else:
            failed_docs += 1
            print(f"   ✗ Failed: {status}")
        
        # Pause between documents to let Ollama recover
        if i < len(docs):
            print("   Waiting 2s before next document...\n")
            time.sleep(2)
    
    # Summary
    print("\n" + "="*50)
    print(f"Done!")
    print(f"  Documents processed: {successful_docs}/{len(docs)}")
    print(f"  Failed: {failed_docs}")
    print(f"  Total chunks indexed: {total_chunks}")
    print("="*50)
    
    if failed_docs > 0:
        print("\nTip: Some documents failed. Try:")
        print("  1. Restart Ollama: brew services restart ollama")
        print("  2. Process failed documents individually")
        print("  3. Close other applications to free memory")

if __name__ == "__main__":
    main()
