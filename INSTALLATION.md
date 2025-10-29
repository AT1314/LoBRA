# LoBRA Installation Guide

## Quick Installation (Recommended)

The fastest way to get LoBRA running - **just one command**:

```bash
cd /path/to/LoBRA
./setup.sh
```

**That's it!** This single script automatically:
1. ✓ Verify all prerequisites
2. ✓ Create Python virtual environment
3. ✓ Install all dependencies
4. ✓ Start Ollama service
5. ✓ Download AI models (llama3.1:8b, nomic-embed-text)
6. ✓ Start Qdrant vector database
7. ✓ Verify the complete installation

**Time required:** 10-15 minutes (mostly downloading AI models)

> **Note:** Don't run `make deps` for initial setup. The `./setup.sh` script already installs all dependencies. Use `make deps` only if you need to reinstall Python packages later.

---

## Manual Installation

If you prefer to install step-by-step or the automatic installation fails:

### Step 1: Install Prerequisites

#### macOS

```bash
# Homebrew (package manager)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Docker Desktop
brew install --cask docker
open -a Docker  # Start Docker Desktop

# Python 3.10+
brew install python

# Ollama (local AI models)
brew install ollama
```

#### Linux

```bash
# Python 3.10+
sudo apt update
sudo apt install python3 python3-pip python3-venv

# Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Ollama
curl -fsSL https://ollama.com/install.sh | sh
```

### Step 2: Start Services

```bash
# Start Ollama
ollama serve  # Keep running in a terminal
# OR run as background service:
brew services start ollama  # macOS
# systemctl start ollama    # Linux

# Start Qdrant vector database
docker run -d --name qdrant \
  -p 6333:6333 \
  -v qdrant_storage:/qdrant/storage \
  qdrant/qdrant:latest
```

### Step 3: Download AI Models

```bash
# Chat model (~4.7GB)
ollama pull llama3.1:8b

# Embedding model (~274MB)
ollama pull nomic-embed-text
```

### Step 4: Install Python Dependencies

```bash
cd /path/to/LoBRA

# Create virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate

# Install dependencies
make deps
```

---

## Verify Installation

After installation (automatic or manual), verify everything works:

```bash
# Check all services
make verify

# Or use the verification script directly
./verify.sh
```

Expected output:
```
✓ Python virtual environment
✓ Python packages
✓ Ollama service
✓ Ollama models
✓ Docker
✓ Qdrant vector DB
✓ vault directory
✓ Configuration
✓ Scripts
```

---

## Test Your Installation

Run a complete end-to-end test:

```bash
make test
```

This will:
1. Verify all services
2. Ingest the example files
3. Run a sample query
4. Display results

---

## Troubleshooting

### Ollama Service Not Running

**Symptom:** `curl http://localhost:11434/api/tags` fails

**Solution:**
```bash
# macOS
brew services start ollama
# OR
ollama serve

# Linux
systemctl start ollama
# OR
ollama serve
```

### Qdrant Not Running

**Symptom:** `curl http://localhost:6333/health` fails

**Solution:**
```bash
# Check if container exists
docker ps -a | grep qdrant

# If exists but stopped
docker start qdrant

# If doesn't exist
docker run -d --name qdrant \
  -p 6333:6333 \
  -v qdrant_storage:/qdrant/storage \
  qdrant/qdrant:latest
```

### Docker Not Running

**Symptom:** `docker ps` fails

**Solution:**
```bash
# macOS
open -a Docker

# Linux
sudo systemctl start docker
```

### Python Dependencies Failed

**Symptom:** Import errors when running scripts

**Solution:**
```bash
# Clean install
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
make deps
```

### Port Already in Use

**Symptom:** "Port 6333 already in use" or "Port 11434 already in use"

**Solution:**
```bash
# Find what's using the port
lsof -i :6333  # or :11434

# Kill the process or stop the service
# For Qdrant:
docker stop qdrant
docker rm qdrant
# Then restart
```

---

## System Requirements

### Minimum
- **OS:** macOS 10.15+, Ubuntu 20.04+, or similar Linux
- **RAM:** 8GB (16GB recommended)
- **Storage:** 10GB free space
- **Internet:** Required for initial setup (downloading models)

### Recommended
- **RAM:** 16GB+ for better performance
- **Storage:** 20GB+ if indexing large document collections
- **CPU:** Apple Silicon or modern multi-core x86_64

---

## Uninstallation

To completely remove LoBRA:

```bash
# Stop and remove services
docker stop qdrant
docker rm qdrant
docker volume rm qdrant_storage

# Stop Ollama
brew services stop ollama  # macOS
# systemctl stop ollama    # Linux

# Remove Python environment
rm -rf .venv

# Remove indexed data
rm -rf brain/* logs/*

# Optional: Remove Ollama models (frees ~5GB)
ollama rm llama3.1:8b
ollama rm nomic-embed-text
```

---

## Next Steps

After successful installation:

1. **Read the Quick Start Guide:** `QUICKSTART.md`
2. **Add your knowledge:** Place files in `vault/`
3. **Index:** `make ingest`
4. **Query:** `make ask q="your question"`

For detailed usage instructions, see `README.md`.

