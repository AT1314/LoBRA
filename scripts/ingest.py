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
Settings.embed_model = OllamaEmbedding(
    model_name=CFG["embed_model"], base_url="http://localhost:11434"
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
    vstore = QdrantVectorStore(client=client, collection_name=COLL)
    storage = StorageContext.from_defaults(vector_store=vstore)

    # Build / refresh index
    print(f"==> Indexing {len(nodes)} chunks into collection '{COLL}'…")
    _ = VectorStoreIndex(nodes, storage_context=storage)

    print("Done. Indexed chunks:", len(nodes))

if __name__ == "__main__":
    main()

