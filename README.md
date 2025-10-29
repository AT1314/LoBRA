# LoBRA - Local Brain Assistant

A local RAG (Retrieval-Augmented Generation) system that learns from your knowledge base and answers questions with citations.

## Features

- 📚 **Multi-format support**: Markdown (with YAML front-matter), PDFs, text files, code snippets
- 🔄 **Auto-conversion pipeline**: Convert Word, PowerPoint, Excel, HTML, EPUB, and images to markdown
- 🔍 **Hybrid retrieval**: Combines BM25 keyword search + semantic embeddings for better accuracy
- 🎯 **Source citations**: All answers include file path citations
- 🏠 **Fully local**: Runs entirely on your machine with Ollama (no API keys needed)
- ⚡ **Fast indexing**: Efficient chunking and vector storage with Qdrant
- 🔒 **Privacy-first**: Your data never leaves your machine

## 💻 Hardware Requirements

LoBRA works great on modest hardware! ✨

- **8GB RAM** (M1 MacBook Air) ✓ Fully supported with optimized config
- **16GB RAM** - Recommended for larger models
- **32GB+ RAM** - Can run the most capable models

**Your configuration has been optimized for 8GB M1 systems!**  
→ Quick tips: `8GB-QUICKREF.md`  
→ Detailed guide: `HARDWARE.md`

## Quick Start

### One-Time Setup (Automated - Recommended)

For first-time installation, run the setup script:

```bash
chmod +x setup.sh
./setup.sh
```

**This is all you need!** The script handles everything:
- ✓ Check all prerequisites (Python, Docker, Ollama)
- ✓ Create Python virtual environment
- ✓ Install all dependencies
- ✓ Download required AI models (~5GB, takes 5-10 minutes)
- ✓ Start Qdrant vector database
- ✓ Verify the installation

**Time:** ~10-15 minutes depending on your internet speed

### Manual Setup (if automated setup fails)

<details>
<summary>Click to expand manual setup instructions</summary>

**Note:** The manual setup below is only needed if `./setup.sh` doesn't work for your system. The automated setup is much easier and handles everything for you.

#### 1. Install Prerequisites (macOS)

```bash
# Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Docker Desktop
brew install --cask docker
open -a Docker

# Python 3.10+
brew install python

# Ollama
brew install ollama
ollama serve  # or: brew services start ollama
```

#### 2. Pull AI Models

```bash
ollama pull llama3.1:8b
ollama pull nomic-embed-text
```

#### 3. Start Qdrant

```bash
docker run -d --name qdrant \
  -p 6333:6333 \
  -v qdrant_storage:/qdrant/storage \
  qdrant/qdrant:latest
```

#### 4. Install Python Dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
make deps
```

</details>

## Usage

### 1. Add Your Knowledge

**Option A: Direct placement** (for markdown, PDFs, text)

Place your files in the `vault/` directory:

```bash
vault/
  ├── machine-learning-notes.md
  ├── research-paper.pdf
  ├── course-notes.md
  └── code-snippets/
      └── algorithms.py
```

**Option B: Auto-conversion** (for Word, PowerPoint, Excel, etc.)

Use the data pipeline to convert other formats:

```bash
# One-time setup
make install-pipeline

# Drop files in inbox/
cp presentation.pptx inbox/
cp notes.docx inbox/
cp data.xlsx inbox/

# Convert to markdown
make pipeline
```

Supported formats: `.docx`, `.pptx`, `.xlsx`, `.html`, `.epub`, `.png` (OCR), and more!  
See `PIPELINE.md` for details.

**Tip**: Use YAML front-matter in Markdown files for better organization:

```yaml
---
title: "Machine Learning Fundamentals"
date: 2025-10-28
tags: [ml, deep-learning, neural-networks]
course: CS229
project: "ML-Research"
summary: "Introduction to supervised and unsupervised learning"
---

# Your content here...
```

### 2. Index Your Knowledge

```bash
make ingest
```

This will process all files and create a searchable index.

### 3. Ask Questions

```bash
make ask q="Summarize my notes on neural networks"
make ask q="What did I learn about transformers?"
make ask q="Explain the KV cache optimization strategy"
```

### 4. Update Your Knowledge

When you add new files or modify existing ones:

```bash
make ingest  # Re-index (idempotent)
```

## Project Structure

```
LoBRA/
├── inbox/                # Drop files here for auto-conversion
├── vault/                # Your knowledge base (markdown, PDFs)
├── processed/            # Converted originals (archive)
├── brain/                # Indexed data (auto-generated)
├── logs/                 # System logs
├── scripts/
│   ├── ingest.py        # Indexing script
│   ├── query.py         # Query script
│   └── preprocess.py    # Format conversion pipeline
├── config.yaml          # Configuration (optimized for 8GB)
├── config-8gb.yaml      # 8GB RAM preset
├── config-16gb.yaml     # 16GB RAM preset
├── requirements.txt     # Core Python dependencies
├── requirements-pipeline.txt  # Format converter dependencies
├── Makefile            # Convenient commands
├── setup.sh            # Auto-setup script (detects your hardware!)
├── verify.sh           # Health check script
├── test-system.sh      # End-to-end test
├── README.md           # Main documentation
├── QUICKSTART.md       # Daily usage guide
├── PIPELINE.md         # Data conversion guide ⭐ NEW
├── HARDWARE.md         # Hardware optimization guide
└── INSTALLATION.md     # Installation instructions
```

## Configuration

**Default:** Optimized for 8GB RAM (your system!)

`config.yaml` is already configured for optimal performance on your M1 MacBook Air:

```yaml
# AI models (memory-efficient)
chat_model: "llama3.2:3b"       # Fast, only ~2GB RAM
embed_model: "nomic-embed-text"  # Lightweight embeddings

# Chunking (optimized for 8GB)
chunk_size: 512      # Balanced size
chunk_overlap: 100   # Efficient overlap

# Retrieval (performance-tuned)
top_k_vector: 5      # Semantic matches
top_k_bm25: 5        # Keyword matches
fusion_k: 6          # Final merged results
```

**Have more RAM?** Use preset configs:
```bash
# For 16GB+ systems (better quality, slower)
cp config-16gb.yaml config.yaml

# Back to 8GB optimized (faster)
cp config-8gb.yaml config.yaml
```

**Need help?** See `HARDWARE.md` for detailed optimization guides.

## Available Commands

```bash
# Setup & Health
make setup              # Run complete automated setup (first time only)
make verify             # Check if all services are running
make test               # Run end-to-end system test
make deps               # Install Python dependencies only (after setup.sh)

# Data Pipeline (convert various formats)
make install-pipeline   # Install format converters (one-time)
make pipeline           # Convert files from inbox/ to vault/
make watch              # Auto-process new files (continuous mode)

# Knowledge Management
make ingest             # Index vault/ contents
make ask                # Query your knowledge base
make clean              # Remove index and logs
```

**Note:** For first-time setup, use `./setup.sh` instead of `make deps`. The setup script does everything including dependencies, services, and models. Use `make deps` only when you need to reinstall Python packages after initial setup.

## How It Works

1. **Ingestion**: Files are chunked, metadata is extracted, and embeddings are generated
2. **Hybrid Retrieval**: When you ask a question:
   - Semantic search finds conceptually similar content
   - BM25 finds keyword matches
   - RRF (Reciprocal Rank Fusion) combines both for optimal results
3. **Response Generation**: The LLM generates answers using retrieved context with source citations

## Advanced Usage

### Filter by Metadata

Modify `scripts/query.py` to filter by course, project, or tags:

```python
# Example: only search CS229 course notes
filters = {"course": "CS229"}
```

### Use Different Models

```bash
# List available models
ollama list

# Pull a new model
ollama pull mistral:7b

# Update config.yaml to use it
chat_model: "mistral:7b"
```

### Monitor Services

```bash
# Check Qdrant health
curl http://localhost:6333/health

# View Qdrant logs
docker logs qdrant

# Check Ollama models
ollama list
```

## Troubleshooting

### Ollama not responding
```bash
# Check if running
curl http://localhost:11434/api/tags

# Start manually
ollama serve
```

### Qdrant connection error
```bash
# Check if container is running
docker ps | grep qdrant

# Start container
docker start qdrant
```

### Python dependencies issues
```bash
# Reinstall dependencies
rm -rf .venv
make deps
```

## Future Enhancements

- 🎨 Web UI (FastAPI/Streamlit)
- 🔄 Incremental indexing (hash-based change detection)
- 🎯 Cross-encoder reranking for higher precision
- 📊 Evaluation harness (MRR, Recall@k)
- 🏷️ Advanced metadata filtering
- 💬 Conversation memory
- 📈 Query analytics and logging

## License

MIT

## Contributing

Contributions welcome! Please open an issue or PR.
