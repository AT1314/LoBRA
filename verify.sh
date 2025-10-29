#!/usr/bin/env bash

# LoBRA Environment Verification Script
# Quick check to ensure all services are running

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo ""
echo "╔═══════════════════════════════════════════════════════╗"
echo "║        LoBRA Environment Verification                ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""

# Track status
all_good=true

# Check Python virtual environment
echo -n "Checking Python virtual environment... "
if [ -d ".venv" ]; then
    echo -e "${GREEN}✓${NC}"
else
    echo -e "${RED}✗${NC}"
    echo "  → Run: python3 -m venv .venv"
    all_good=false
fi

# Check Python packages
echo -n "Checking Python packages... "
if [ -d ".venv" ]; then
    source .venv/bin/activate
    if python3 -c "import llama_index.core" 2>/dev/null; then
        echo -e "${GREEN}✓${NC}"
    else
        echo -e "${RED}✗${NC}"
        echo "  → Run: make deps"
        all_good=false
    fi
else
    echo -e "${YELLOW}⊘${NC} (venv not found)"
    all_good=false
fi

# Check Ollama service
echo -n "Checking Ollama service... "
if curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
    echo -e "${GREEN}✓${NC}"
else
    echo -e "${RED}✗${NC}"
    echo "  → Run: ollama serve (or brew services start ollama)"
    all_good=false
fi

# Check Ollama models
echo -n "Checking Ollama models... "
if command -v ollama >/dev/null 2>&1; then
    models=$(ollama list 2>/dev/null | tail -n +2)
    if echo "$models" | grep -q "llama3.1:8b" && echo "$models" | grep -q "nomic-embed-text"; then
        echo -e "${GREEN}✓${NC}"
    else
        echo -e "${YELLOW}⚠${NC}"
        echo "  → Missing models. Run:"
        if ! echo "$models" | grep -q "llama3.1:8b"; then
            echo "    ollama pull llama3.1:8b"
        fi
        if ! echo "$models" | grep -q "nomic-embed-text"; then
            echo "    ollama pull nomic-embed-text"
        fi
        all_good=false
    fi
else
    echo -e "${RED}✗${NC}"
    all_good=false
fi

# Check Docker
echo -n "Checking Docker... "
if command -v docker >/dev/null 2>&1; then
    if docker info >/dev/null 2>&1; then
        echo -e "${GREEN}✓${NC}"
    else
        echo -e "${RED}✗${NC}"
        echo "  → Docker not running. Start Docker Desktop."
        all_good=false
    fi
else
    echo -e "${RED}✗${NC}"
    echo "  → Docker not installed"
    all_good=false
fi

# Check Qdrant
echo -n "Checking Qdrant vector DB... "
if curl -s http://localhost:6333/health >/dev/null 2>&1; then
    echo -e "${GREEN}✓${NC}"
else
    echo -e "${RED}✗${NC}"
    if docker ps -a --format '{{.Names}}' | grep -q "^qdrant$"; then
        echo "  → Container exists but not running. Run: docker start qdrant"
    else
        echo "  → Run: docker run -d --name qdrant -p 6333:6333 -v qdrant_storage:/qdrant/storage qdrant/qdrant:latest"
    fi
    all_good=false
fi

# Check vault directory
echo -n "Checking vault directory... "
if [ -d "vault" ]; then
    file_count=$(find vault -type f 2>/dev/null | wc -l | tr -d ' ')
    echo -e "${GREEN}✓${NC} (${file_count} files)"
    if [ "$file_count" -eq 0 ]; then
        echo "  ${YELLOW}Note:${NC} vault/ is empty. Add some files to index."
    fi
else
    echo -e "${YELLOW}⚠${NC}"
    echo "  → Creating vault/ directory..."
    mkdir -p vault
fi

# Check config
echo -n "Checking configuration... "
if [ -f "config.yaml" ]; then
    echo -e "${GREEN}✓${NC}"
else
    echo -e "${RED}✗${NC}"
    echo "  → config.yaml missing!"
    all_good=false
fi

# Check scripts
echo -n "Checking scripts... "
if [ -f "scripts/ingest.py" ] && [ -f "scripts/query.py" ]; then
    echo -e "${GREEN}✓${NC}"
else
    echo -e "${RED}✗${NC}"
    echo "  → Missing scripts!"
    all_good=false
fi

echo ""
echo "────────────────────────────────────────────────────────"

if [ "$all_good" = true ]; then
    echo -e "${GREEN}✓ All systems operational!${NC}"
    echo ""
    echo "You're ready to use LoBRA:"
    echo "  1. Add files to vault/"
    echo "  2. Run: make ingest"
    echo "  3. Run: make ask q=\"your question\""
    echo ""
else
    echo -e "${RED}✗ Some issues found.${NC} Please fix them before using LoBRA."
    echo ""
    echo "Quick fix: Run ./setup.sh to auto-configure everything."
    echo ""
    exit 1
fi

