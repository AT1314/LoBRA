# LoBRA Quick Start Guide

## Installation (First Time Only)

```bash
# Clone or navigate to LoBRA directory
cd /path/to/LoBRA

# Run automated setup
chmod +x setup.sh
./setup.sh
```

The setup script will:
- ✓ Check prerequisites (Python, Docker, Ollama)
- ✓ Create virtual environment
- ✓ Install all dependencies
- ✓ Download AI models (~5-10 minutes)
- ✓ Start Qdrant vector database
- ✓ Verify everything works

### 🤔 Setup vs. Dependencies: What's the Difference?

| Command | What it does | When to use |
|---------|-------------|-------------|
| `./setup.sh` | **Complete setup**: prerequisites, venv, dependencies, services, models | ✅ First time installation<br>✅ Full reconfiguration |
| `make deps` | **Only Python packages**: Creates venv + installs requirements.txt | ⚠️ After setup.sh<br>⚠️ Updating packages only |

**TLDR:** Use `./setup.sh` for first-time setup. It does everything, including what `make deps` does!

### 💡 Your 8GB M1 System

Good news! Your configuration is already optimized for your hardware:
- ✅ Using lightweight model (llama3.2:3b - only 2GB RAM)
- ✅ Memory-efficient settings (512 token chunks)
- ✅ Qdrant limited to 1GB RAM
- ✅ Apple Silicon GPU acceleration enabled

**See `8GB-QUICKREF.md` for quick tips specific to your hardware.**

## Daily Usage

### Step 1: Activate Environment
```bash
source .venv/bin/activate
```

### Step 2: Add Your Files
Place files in `vault/`:
```bash
cp ~/my-notes.md vault/
cp ~/research.pdf vault/
```

### Step 3: Index Your Knowledge
```bash
make ingest
```

### Step 4: Ask Questions
```bash
make ask q="Summarize my notes on machine learning"
make ask q="What are the key concepts in my research papers?"
```

## Common Commands

| Command | Description |
|---------|-------------|
| `make deps` | Install/update dependencies |
| `make ingest` | Index all files in vault/ |
| `make ask q="..."` | Query your knowledge base |
| `make clean` | Remove index and logs |

## File Organization Tips

### Use Front-Matter in Markdown
```yaml
---
title: "Neural Networks Fundamentals"
date: 2025-10-29
tags: [ml, deep-learning]
course: CS229
project: "ML-Research"
summary: "Core concepts of neural networks"
---

# Your content here...
```

### Organize by Topics
```
vault/
├── courses/
│   ├── cs229/
│   └── cs231n/
├── research/
│   ├── papers/
│   └── experiments/
└── projects/
    └── current/
```

## Troubleshooting

### Services Not Running

**Check Ollama:**
```bash
curl http://localhost:11434/api/tags
# If fails: ollama serve
```

**Check Qdrant:**
```bash
curl http://localhost:6333/health
# If fails: docker start qdrant
```

**Check Docker:**
```bash
docker ps
# If empty: open -a Docker
```

### Re-run Setup
```bash
# If something breaks, re-run:
./setup.sh
```

### Clean Install
```bash
# Remove everything and start fresh:
make clean
rm -rf .venv
docker rm -f qdrant
./setup.sh
```

## Example Workflow

```bash
# 1. Morning: Activate environment
source .venv/bin/activate

# 2. Add yesterday's notes
cp ~/Documents/notes/*.md vault/course-notes/

# 3. Index new content
make ingest

# 4. Query for review
make ask q="What did I learn about transformers?"
make ask q="Summarize key points from yesterday's lecture"

# 5. Before exam: comprehensive review
make ask q="List all important algorithms from CS229"
make ask q="Explain the main concepts from my neural network notes"
```

## Performance Tips

- **Chunk size**: 700 tokens balances context vs. precision
- **Hybrid retrieval**: Handles both concepts and exact terms
- **Citations**: Always check source files for full context
- **Re-index regularly**: After adding multiple files

## Advanced

### Change Models
```bash
# List available
ollama list

# Pull new model
ollama pull mistral:7b

# Edit config.yaml
chat_model: "mistral:7b"
```

### Monitor Services
```bash
# Qdrant dashboard
open http://localhost:6333/dashboard

# Qdrant logs
docker logs qdrant

# Ollama models
ollama list
```

### Custom Configuration
Edit `config.yaml`:
- `chunk_size`: Text chunk size (default: 700)
- `top_k_vector`: Number of semantic results (default: 6)
- `top_k_bm25`: Number of keyword results (default: 6)
- `fusion_k`: Final results after merging (default: 8)

## Getting Help

- Check `README.md` for full documentation
- Look at `vault/example-note.md` for markdown examples
- Run `./setup.sh` if services aren't working
- Check logs in `logs/` directory

---

**Remember**: Everything runs locally. Your data never leaves your machine! 🔒

