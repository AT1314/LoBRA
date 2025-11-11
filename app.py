#!/usr/bin/env python3
"""
LoBRA - Local Brain Assistant Web UI
Simple Streamlit interface for querying your knowledge base
"""

import streamlit as st
import yaml
from pathlib import Path
import time

from llama_index.core import Settings, VectorStoreIndex, StorageContext
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from llama_index.retrievers.bm25 import BM25Retriever

# Page config
st.set_page_config(
    page_title="LoBRA - Local Brain Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .source-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .chunk-text {
        background-color: #ffffff;
        padding: 1rem;
        border-left: 3px solid #4CAF50;
        margin: 0.5rem 0;
    }
    .stTextInput > div > div > input {
        font-size: 1.1rem;
    }
</style>
""", unsafe_allow_html=True)

# Load config
@st.cache_resource
def load_config():
    return yaml.safe_load(open("config.yaml"))

@st.cache_resource
def initialize_system():
    """Initialize LoBRA system"""
    cfg = load_config()
    
    # Setup models
    Settings.llm = Ollama(
        model=cfg["chat_model"], 
        base_url="http://localhost:11434",
        request_timeout=120.0  # 2 minute timeout
    )
    Settings.embed_model = OllamaEmbedding(
        model_name=cfg["embed_model"], 
        base_url="http://localhost:11434"
    )
    
    # Connect to vector store
    client = QdrantClient(url=cfg["qdrant_url"])
    vstore = QdrantVectorStore(client=client, collection_name=cfg["collection_name"])
    storage = StorageContext.from_defaults(vector_store=vstore)
    index = VectorStoreIndex.from_vector_store(vstore)
    
    return cfg, index

def rrf(rankings, k=60):
    """Reciprocal Rank Fusion"""
    scores = {}
    for rlist in rankings:
        for rank, doc_id in enumerate(rlist, start=1):
            scores[doc_id] = scores.get(doc_id, 0.0) + 1.0 / (k + rank)
    return [doc for doc, _ in sorted(scores.items(), key=lambda x: x[1], reverse=True)]

def query_brain(question, cfg, index):
    """Query the knowledge base"""
    
    # Vector retrieval
    vector_retriever = index.as_retriever(similarity_top_k=cfg["top_k_vector"])
    vnodes = vector_retriever.retrieve(question)
    
    # BM25 retrieval (with fallback)
    bnodes = []
    try:
        bm25 = BM25Retriever.from_defaults(
            docstore=index.docstore, 
            similarity_top_k=cfg["top_k_bm25"]
        )
        bnodes = bm25.retrieve(question)
    except:
        pass  # Fall back to vector-only
    
    # Fuse results
    v_ids = [n.node.node_id for n in vnodes]
    b_ids = [n.node.node_id for n in bnodes]
    
    if b_ids:
        fused_ids = rrf([v_ids, b_ids])[:cfg["fusion_k"]]
    else:
        fused_ids = v_ids[:cfg["fusion_k"]]
    
    # Get fused nodes
    id2node = {n.node.node_id: n.node for n in vnodes + bnodes}
    fused_nodes = [id2node[i] for i in fused_ids if i in id2node]
    
    # Build context with citations
    context_blocks = []
    seen = set()
    sources = []
    
    for n in fused_nodes:
        src = (n.metadata or {}).get("source_path", "unknown")
        if src not in seen:
            seen.add(src)
            context_blocks.append(f"[{src}]\n{n.get_content()[:800]}")
            sources.append({
                "path": src,
                "text": n.get_content()[:500]
            })
    
    context = "\n\n---\n\n".join(context_blocks)
    
    # Generate response
    prompt = f"""You are a helpful assistant. Use the CONTEXT to answer the question.
Cite sources as bullet points with file paths. Be concise and accurate.

QUESTION:
{question}

CONTEXT:
{context}
"""
    
    response = Settings.llm.complete(prompt)
    
    return response.text, sources, fused_nodes

# Header
st.markdown('<div class="main-header">🧠 LoBRA</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Local Brain Assistant - Query Your Knowledge Base</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    try:
        cfg = load_config()
        st.success("✅ System Ready")
        
        st.metric("Chat Model", cfg["chat_model"])
        st.metric("Embedding Model", cfg["embed_model"])
        st.metric("Chunk Size", cfg["chunk_size"])
        
        st.divider()
        
        st.header("📊 System Info")
        vault_path = Path(cfg["vault_path"])
        if vault_path.exists():
            md_files = list(vault_path.rglob("*.md"))
            pdf_files = list(vault_path.rglob("*.pdf"))
            st.metric("Markdown Files", len(md_files))
            st.metric("PDF Files", len(pdf_files))
        
        st.divider()
        
        st.header("📚 Quick Tips")
        st.info("""
**Ask questions like:**
- "Summarize my notes on X"
- "What did I learn about Y?"
- "Explain the concept of Z"
- "Show examples of W"
        """)
        
        st.divider()
        
        if st.button("🔄 Refresh Index", help="Re-index your vault"):
            st.info("Run `make ingest` in terminal to update the index")
            
    except Exception as e:
        st.error(f"⚠️ Configuration error: {e}")
        st.stop()

# Initialize system
try:
    with st.spinner("Loading LoBRA system..."):
        cfg, index = initialize_system()
except Exception as e:
    st.error(f"❌ Failed to initialize system: {e}")
    st.error("Make sure Ollama and Qdrant are running!")
    st.stop()

# Main interface
st.header("💬 Ask Your Brain")

# Query input
question = st.text_input(
    "What would you like to know?",
    placeholder="e.g., Explain METIS or Summarize my machine learning notes",
    key="question_input"
)

# Search button
col1, col2 = st.columns([1, 5])
with col1:
    search_button = st.button("🔍 Search", type="primary", use_container_width=True)

# Query execution
if search_button and question:
    with st.spinner("🤔 Thinking..."):
        try:
            start_time = time.time()
            answer, sources, nodes = query_brain(question, cfg, index)
            elapsed = time.time() - start_time
            
            # Display answer
            st.success(f"✅ Answer generated in {elapsed:.1f}s")
            
            st.markdown("### 📝 Answer")
            st.markdown(answer)
            
            # Display sources
            st.markdown("### 📚 Sources")
            
            if sources:
                for i, source in enumerate(sources, 1):
                    with st.expander(f"📄 {Path(source['path']).name}", expanded=i==1):
                        st.markdown(f"**Path:** `{source['path']}`")
                        st.markdown("**Excerpt:**")
                        st.markdown(f'<div class="chunk-text">{source["text"]}...</div>', unsafe_allow_html=True)
            else:
                st.info("No sources found")
            
            # Display relevance scores
            if nodes:
                st.markdown("### 🎯 Relevance Scores")
                for i, node in enumerate(nodes[:5], 1):
                    score = getattr(node, 'score', 0.0)
                    src = (node.node.metadata or {}).get("source_path", "unknown")
                    st.progress(score, text=f"{i}. {Path(src).name} - Score: {score:.3f}")
                    
        except Exception as e:
            st.error(f"❌ Error: {e}")
            st.error("Check terminal for detailed error messages")

elif search_button and not question:
    st.warning("⚠️ Please enter a question")

# Example queries
st.markdown("---")
st.markdown("### 💡 Example Queries")

st.info("""
Try these example questions:
- "Summarize my notes on GPU programming"
- "What are the key concepts in machine learning from my notes?"
- "Explain METIS from my research notes"
- "List the research papers I've taken notes on"
- "Compare Triton and TVM"
""")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "LoBRA - Your Local Brain Assistant | Built with ❤️ using LlamaIndex & Streamlit"
    "</div>",
    unsafe_allow_html=True
)

