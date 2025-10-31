import os, sys, yaml, frontmatter, time
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

# ---- models
# Configure embedding model with conservative settings for 8GB RAM
Settings.embed_model = OllamaEmbedding(
    model_name=CFG["embed_model"], 
    base_url="http://localhost:11434",
    # Reduce internal batching to avoid memory issues
    embed_batch_size=1,  # Process one embedding at a time
)
Settings.llm = Ollama(model=CFG["chat_model"], base_url="http://localhost:11434")

# ---- text splitter
splitter = SentenceSplitter(
    chunk_size=CFG["chunk_size"],
    chunk_overlap=CFG["chunk_overlap"],
)

# ---- helpers
def read_markdown_with_frontmatter(fp: Path):
    post = frontmatter.load(fp)
    content = post.content
    meta = {k: post.get(k) for k in CFG["frontmatter_keys"] if k in post}
    return content, meta

def load_docs(vault: Path):
    # LlamaIndex can read many types, but we manually handle MD to keep front-matter metadata.
    md_files, other_files = [], []
    for p in vault.rglob("*"):
        if p.is_file():
            if p.suffix.lower() in [".md", ".markdown"]:
                md_files.append(p)
            else:
                other_files.append(p)

    docs = []

    # Markdown with front-matter
    for fp in tqdm(md_files, desc="Markdown"):
        text, meta = read_markdown_with_frontmatter(fp)
        meta.update({
            "source_path": str(fp),
            "ext": fp.suffix.lower(),
            "mod_time": int(fp.stat().st_mtime),
        })
        docs.append(Document(text=text, metadata=meta))

    # Other (PDF, txt, etc.)
    if other_files:
        reader = SimpleDirectoryReader(
            input_files=[str(p) for p in other_files],
            recursive=False,
        )
        for d in tqdm(reader.load_data(), desc="Other files"):
            # augment metadata
            md = dict(d.metadata or {})
            md.update({"source_path": md.get("file_path", md.get("source", ""))})
            d.metadata = md
            docs.append(d)

    return docs

def main():
    if not VAULT.exists():
        print(f"Vault path {VAULT} not found. Create it and add files.", file=sys.stderr)
        sys.exit(1)

    print("==> Loading documents...")
    docs = load_docs(VAULT)
    if not docs:
        print("No documents found in vault/ . Add .md/.pdf/etc. and re-run.")
        sys.exit(0)

    # Split into nodes
    print("==> Splitting into chunks...")
    nodes = []
    for d in tqdm(docs, desc="Chunking"):
        for n in splitter.get_nodes_from_documents([d]):
            nodes.append(n)

    # Setup Qdrant
    print("==> Connecting Qdrant…")
    client = QdrantClient(url=QDRANT_URL)
    
    # Check if collection exists and might be corrupted
    collections = client.get_collections().collections
    collection_exists = any(c.name == COLL for c in collections)
    
    # Option to clear corrupted index (uncomment if needed):
    # if collection_exists:
    #     print(f"   Clearing existing collection '{COLL}' due to previous errors...")
    #     client.delete_collection(COLL)
    #     collection_exists = False
    
    vstore = QdrantVectorStore(client=client, collection_name=COLL)
    storage = StorageContext.from_defaults(vector_store=vstore)

    # Build / refresh index with batching for memory efficiency (important for 8GB RAM)
    print(f"==> Indexing {len(nodes)} chunks into collection '{COLL}'…")
    
    # For large batches on 8GB systems, process in smaller chunks
    # This prevents memory exhaustion during embedding generation
    # Process ONE chunk at a time for maximum stability on 8GB RAM
    # LlamaIndex may batch internally, so we process sequentially
    BATCH_SIZE = 1  # One chunk at a time to avoid overwhelming Ollama
    
    if len(nodes) > 100:
        print(f"   Large batch detected ({len(nodes)} chunks). Processing in batches of {BATCH_SIZE}...")
        try:
            # Try to load existing index first
            try:
                index = VectorStoreIndex.from_vector_store(vstore)
                print("   Found existing index, adding new chunks...")
            except:
                # No existing index, create empty one
                index = VectorStoreIndex.from_documents([], storage_context=storage)
                print("   Creating new index...")
            
            # Process in batches with retry logic
            successful_chunks = 0
            failed_chunks = 0
            
            for i in tqdm(range(0, len(nodes), BATCH_SIZE), desc="Batching"):
                batch = nodes[i:i + BATCH_SIZE]
                max_retries = 3
                retry_count = 0
                success = False
                
                while retry_count < max_retries and not success:
                    try:
                        # Use insert_nodes for incremental indexing
                        # Process one chunk at a time with health checks
                        for node in batch:
                            # Verify Ollama is still responding before each embedding
                            try:
                                import requests
                                health = requests.get("http://localhost:11434/api/tags", timeout=2)
                                if health.status_code != 200:
                                    raise Exception("Ollama health check failed")
                            except:
                                print(f"\n   Ollama not responding, waiting 3s...")
                                time.sleep(3)
                            
                            # Insert single node
                            index.insert_nodes([node])
                            successful_chunks += 1
                            time.sleep(0.5)  # Delay between each chunk - increased for stability
                            
                            # Every 10 chunks, longer pause to let Ollama recover
                            if successful_chunks % 10 == 0:
                                time.sleep(2.0)
                        
                        success = True
                        time.sleep(1.5)  # Longer delay after batch
                        break
                    except AttributeError:
                        # Fallback: rebuild index with accumulated nodes
                        print(f"\n   Rebuilding index with {successful_chunks + len(batch)} nodes...")
                        all_nodes_so_far = nodes[:successful_chunks + len(batch)]
                        try:
                            index = VectorStoreIndex(all_nodes_so_far, storage_context=storage)
                            successful_chunks += len(batch)
                            success = True
                            break
                        except Exception as rebuild_error:
                            print(f"   Rebuild also failed: {rebuild_error}")
                            failed_chunks += len(batch)
                            success = False
                            break
                    except Exception as e:
                        retry_count += 1
                        wait_time = 2 ** retry_count  # Exponential backoff: 2s, 4s, 8s
                        if retry_count < max_retries:
                            print(f"\n   Batch {i//BATCH_SIZE + 1} failed (attempt {retry_count}/{max_retries}): {str(e)[:100]}")
                            print(f"   Waiting {wait_time}s before retry...")
                            time.sleep(wait_time)
                            
                            # Try restarting Ollama connection
                            try:
                                Settings.embed_model = OllamaEmbedding(
                                    model_name=CFG["embed_model"], base_url="http://localhost:11434"
                                )
                            except:
                                pass
                        else:
                            print(f"\n   Batch {i//BATCH_SIZE + 1} failed after {max_retries} attempts")
                            failed_chunks += len(batch)
                
                if not success:
                    time.sleep(2)  # Longer delay after failure
            
            print(f"\nDone. Successfully indexed: {successful_chunks} chunks")
            if failed_chunks > 0:
                print(f"Failed: {failed_chunks} chunks")
                print("\nTip: Try processing fewer documents at once, or restart Ollama:")
                print("  brew services restart ollama")
        except Exception as e:
            print(f"\nError during batch indexing: {e}", file=sys.stderr)
            print("\nTroubleshooting tips:", file=sys.stderr)
            print("  1. Check Ollama: curl http://localhost:11434/api/tags", file=sys.stderr)
            print("  2. Restart Ollama: brew services restart ollama", file=sys.stderr)
            print("  3. Free memory: Close other applications", file=sys.stderr)
            print("  4. Reduce batch size in ingest.py (currently {BATCH_SIZE})", file=sys.stderr)
            sys.exit(1)
    else:
        # Small batch, process all at once
        try:
            index = VectorStoreIndex(nodes, storage_context=storage, show_progress=True)
            print("Done. Indexed chunks:", len(nodes))
        except Exception as e:
            print(f"\nError during indexing: {e}", file=sys.stderr)
            print("\nTroubleshooting tips:", file=sys.stderr)
            print("  1. Check Ollama: curl http://localhost:11434/api/tags", file=sys.stderr)
            print("  2. Restart Ollama: brew services restart ollama", file=sys.stderr)
            print("  3. Verify embedding model: ollama list", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    main()


