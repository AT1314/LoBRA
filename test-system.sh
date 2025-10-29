#!/usr/bin/env bash

# Quick system test for LoBRA
# This script runs a simple end-to-end test

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo ""
echo "╔═══════════════════════════════════════════════════════╗"
echo "║            LoBRA System Test                         ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""

# Activate virtual environment
if [ ! -d ".venv" ]; then
    echo -e "${RED}Error: Virtual environment not found. Run ./setup.sh first.${NC}"
    exit 1
fi

source .venv/bin/activate

# Check if vault has files
file_count=$(find vault -type f -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
if [ "$file_count" -eq 0 ]; then
    echo -e "${RED}Error: No markdown files in vault/. Please add some files first.${NC}"
    exit 1
fi

echo -e "${BLUE}[1/3]${NC} Verifying services..."
./verify.sh > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo -e "      ${GREEN}✓${NC} All services running"
else
    echo -e "      ${RED}✗${NC} Services check failed"
    exit 1
fi

echo -e "${BLUE}[2/3]${NC} Running ingestion..."
make ingest
if [ $? -eq 0 ]; then
    echo -e "      ${GREEN}✓${NC} Ingestion successful"
else
    echo -e "      ${RED}✗${NC} Ingestion failed"
    exit 1
fi

echo -e "${BLUE}[3/3]${NC} Testing query..."
result=$(make ask q="What topics are covered in my notes?" 2>/dev/null)
if [ $? -eq 0 ]; then
    echo -e "      ${GREEN}✓${NC} Query successful"
    echo ""
    echo "────────────────────────────────────────────────────────"
    echo "Sample query result:"
    echo "────────────────────────────────────────────────────────"
    echo "$result" | head -20
    echo ""
    echo "────────────────────────────────────────────────────────"
else
    echo -e "      ${RED}✗${NC} Query failed"
    exit 1
fi

echo ""
echo -e "${GREEN}✓ System test passed!${NC}"
echo ""
echo "LoBRA is ready to use. Try:"
echo "  make ask q=\"Summarize my notes on machine learning\""
echo ""

