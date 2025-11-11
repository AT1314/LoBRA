import argparse, yaml, math
from llama_index.core import Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding

from qdrant_client import QdrantClient
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.retrievers.bm25 import BM25Retriever

# Simple RRF fusion
def rrf(rankings, k=60):
    # rankings: list of lists of doc_ids in ranked order
    scores = {}
    for rlist in rankings:
        for rank, doc_id in enumerate(rlist, start=1):
            scores[doc_id] = scores.get(doc_id, 0.0) + 1.0 / (k + rank)
    return [doc for doc, _ in sorted(scores.items(), key=lambda x: x[1], reverse=True)]

def main():
    CFG = yaml.safe_load(open("config.yaml"))
    Settings.llm = Ollama(model=CFG["chat_model"], base_url="http://localhost:11434")
    Settings.embed_model = OllamaEmbedding(model_name=CFG["embed_model"], base_url="http://localhost:11434")

    parser = argparse.ArgumentParser()
    parser.add_argument("--q", required=True, help="question")
    args = parser.parse_args()

    # Connect vector store
    client = QdrantClient(url=CFG["qdrant_url"])
    vstore = QdrantVectorStore(client=client, collection_name=CFG["collection_name"])
    storage = StorageContext.from_defaults(vector_store=vstore)
    index = VectorStoreIndex.from_vector_store(vstore)

    # Vector retrieval
    vector_retriever = index.as_retriever(similarity_top_k=CFG["top_k_vector"])
    vnodes = vector_retriever.retrieve(args.q)

    # BM25 retrieval (keyword) - with fallback
    bnodes = []
    try:
        bm25 = BM25Retriever.from_defaults(docstore=index.docstore, similarity_top_k=CFG["top_k_bm25"])
        bnodes = bm25.retrieve(args.q)
    except (ValueError, Exception) as e:
        # BM25 might fail if docstore is empty or improperly structured
        # Fall back to vector-only search
        print(f"Note: BM25 retrieval unavailable, using vector search only", flush=True)
        pass

    # Fuse results with RRF (or use vector-only if BM25 failed)
    v_ids = [n.node.node_id for n in vnodes]
    b_ids = [n.node.node_id for n in bnodes]
    
    if b_ids:
        fused_ids = rrf([v_ids, b_ids])[:CFG["fusion_k"]]
    else:
        # No BM25 results, use vector results only
        fused_ids = v_ids[:CFG["fusion_k"]]

    # Keep fused nodes
    id2node = {n.node.node_id: n.node for n in vnodes + bnodes}
    fused_nodes = [id2node[i] for i in fused_ids if i in id2node]

    # Build a lightweight response with citations
    context_blocks = []
    seen = set()
    for n in fused_nodes:
        src = (n.metadata or {}).get("source_path", "unknown")
        if src not in seen:
            seen.add(src)
            context_blocks.append(f"[{src}]\n{n.get_content()[:800]}")
    context = "\n\n---\n\n".join(context_blocks)

    prompt = f"""You are a helpful assistant. Use the CONTEXT to answer.
Cite sources as bullet points with file paths. Be concise.

QUESTION:
{args.q}

CONTEXT:
{context}
"""
    resp = Settings.llm.complete(prompt)
    print(resp.text)

if __name__ == "__main__":
    main()

