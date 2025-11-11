# LoBRA Web UI Guide

## Overview

LoBRA now includes a beautiful web-based UI built with Streamlit, making it easy to query your knowledge base through a browser.

## Quick Start

### 1. Install UI Dependencies

```bash
make install-ui
```

This installs:
- Streamlit (web framework)
- Watchdog (for auto-reload)

### 2. Launch the UI

```bash
make ui
```

The UI will open in your browser at: **http://localhost:8501**

### 3. Use the Interface

1. **Enter your question** in the text box
2. **Click "Search"** or press Enter
3. **View the answer** with source citations
4. **Explore sources** by expanding the source cards

## Features

### 🎨 Beautiful Interface
- Clean, modern design
- Dark mode support
- Responsive layout

### 💬 Smart Q&A
- Natural language queries
- Context-aware responses
- Source citations with excerpts

### 📊 System Monitoring
- View configuration
- Check vault statistics
- See relevance scores

### 🔍 Quick Examples
- Pre-built example queries
- One-click to try

### 📚 Source Explorer
- View all retrieved sources
- See relevance scores
- Read context excerpts

## Screenshots

### Main Interface
```
┌─────────────────────────────────────────────┐
│  🧠 LoBRA                                   │
│  Local Brain Assistant                      │
├─────────────────────────────────────────────┤
│  💬 Ask Your Brain                          │
│  ┌───────────────────────────────────────┐ │
│  │ What would you like to know?          │ │
│  └───────────────────────────────────────┘ │
│  [🔍 Search]                                │
├─────────────────────────────────────────────┤
│  📝 Answer                                  │
│  [Generated answer with citations]          │
├─────────────────────────────────────────────┤
│  📚 Sources                                 │
│  📄 source1.md [Expand]                    │
│  📄 source2.md [Expand]                    │
└─────────────────────────────────────────────┘
```

## Configuration

The UI automatically reads from `config.yaml`. You can see current settings in the sidebar:

- **Chat Model**: Which LLM is being used
- **Embedding Model**: Vector embedding model
- **Chunk Size**: Text chunking configuration
- **Vault Stats**: Number of files indexed

## Tips & Tricks

### 1. Better Questions Get Better Answers

**Good:**
- "Summarize the key points from my GPU notes"
- "What did I learn about CUDA memory management?"
- "Compare my notes on Triton vs TVM"

**Less Good:**
- "GPU"
- "Tell me stuff"
- "What's in my notes?"

### 2. Use the Sidebar

The sidebar shows:
- System configuration
- Vault statistics
- Quick tips
- Refresh button

### 3. Explore Sources

Click on source cards to:
- See the full file path
- Read context excerpts
- Understand where answers come from

### 4. Check Relevance Scores

Lower scores = less relevant. If scores are low (<0.5), try:
- Rephrasing your question
- Being more specific
- Adding context

## Advanced Usage

### Custom Port

```bash
.venv/bin/python -m streamlit run app.py --server.port 8080
```

### Run in Background

```bash
nohup make ui > logs/ui.log 2>&1 &
```

### Auto-reload on Changes

Streamlit automatically reloads when you modify `app.py`

## Troubleshooting

### UI won't start

**Error**: "Address already in use"
```bash
# Kill existing Streamlit process
pkill -f streamlit
make ui
```

**Error**: "Cannot connect to Ollama"
```bash
# Check Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama if needed
ollama serve
```

### No results found

1. **Check if index exists:**
   ```bash
   curl http://localhost:6333/collections/local_brain
   ```

2. **Re-index your vault:**
   ```bash
   make ingest
   ```

3. **Restart the UI:**
   ```bash
   # Ctrl+C to stop, then:
   make ui
   ```

### Slow responses

**Causes:**
- Large chunks being processed
- LLM model is large
- First query (model loading)

**Solutions:**
1. Wait for first query to complete (LLM loads into memory)
2. Subsequent queries will be faster
3. Consider using a smaller model in `config.yaml`

### "System not initialized"

```bash
# Ensure prerequisites are running
docker ps | grep qdrant    # Should see qdrant container
curl http://localhost:11434/api/tags  # Should return Ollama models

# Re-index if needed
make ingest
```

## Customization

### Change UI Theme

Edit `app.py` and modify the CSS in the `st.markdown()` section:

```python
st.markdown("""
<style>
    /* Your custom styles here */
</style>
""", unsafe_allow_html=True)
```

### Add Custom Features

The UI is built with Streamlit. You can extend `app.py` to add:
- Chat history
- Document upload
- Advanced filters
- Export functionality

### Example: Add Chat History

```python
# In app.py, add session state
if 'history' not in st.session_state:
    st.session_state.history = []

# After generating answer
st.session_state.history.append({
    'question': question,
    'answer': answer,
    'timestamp': time.time()
})

# Display history in sidebar
with st.sidebar:
    st.header("📜 Chat History")
    for item in st.session_state.history[-5:]:
        st.text(f"Q: {item['question'][:50]}")
```

## Alternative UIs

### Option 2: Gradio (Simpler)

If you prefer Gradio:

```bash
pip install gradio
```

Create `app_gradio.py`:
```python
import gradio as gr
from scripts.query import query_brain

def ask(question):
    answer, sources = query_brain(question)
    return answer, "\n\n".join([s['path'] for s in sources])

interface = gr.Interface(
    fn=ask,
    inputs=gr.Textbox(label="Question", placeholder="Ask me anything..."),
    outputs=[
        gr.Textbox(label="Answer"),
        gr.Textbox(label="Sources")
    ],
    title="🧠 LoBRA - Local Brain Assistant",
    theme=gr.themes.Soft()
)

interface.launch()
```

### Option 3: Terminal UI with Rich

For a fancy terminal interface, see `TERMINAL-UI.md` (coming soon)

## Performance

### Typical Response Times

- **First query**: 10-30s (model loading)
- **Subsequent queries**: 3-8s
- **Vector search**: < 1s
- **LLM generation**: 2-7s

### Memory Usage

- **Streamlit app**: ~200-300MB
- **LLM model (llama3.1:8b)**: ~5-6GB
- **Total system**: ~6-8GB RAM

## Security

### Running Locally

The UI runs on `localhost` only by default. To expose:

```bash
streamlit run app.py --server.address 0.0.0.0
```

⚠️ **Warning**: Only do this on a trusted network!

### Authentication

For basic auth, use Streamlit's authentication:

```python
# In app.py
import streamlit_authenticator as stauth

# Add authentication
authenticator = stauth.Authenticate(...)
name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    # Show UI
    pass
```

## Next Steps

1. **Try it out**: `make ui`
2. **Customize**: Edit `app.py` to your liking
3. **Share feedback**: What features would you like?

## Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Streamlit Gallery](https://streamlit.io/gallery)
- [Custom Components](https://streamlit.io/components)

---

Enjoy your new LoBRA UI! 🧠✨

