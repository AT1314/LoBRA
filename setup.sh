#!/usr/bin/env bash

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Print banner
print_banner() {
    echo ""
    echo "╔═══════════════════════════════════════════════════════╗"
    echo "║                                                       ║"
    echo "║           LoBRA - Local Brain Assistant              ║"
    echo "║              Environment Setup Script                ║"
    echo "║                                                       ║"
    echo "╚═══════════════════════════════════════════════════════╝"
    echo ""
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    local missing_deps=()
    
    # Check Python
    if ! command_exists python3; then
        missing_deps+=("python3")
    else
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        PYTHON_MAJOR=$(echo "$PYTHON_VERSION" | cut -d'.' -f1)
        PYTHON_MINOR=$(echo "$PYTHON_VERSION" | cut -d'.' -f2)
        
        # Check for Python 3.14+ compatibility issue
        if [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -ge 14 ]; then
            log_error "Python ${PYTHON_VERSION} is not compatible with llama-index packages"
            echo ""
            echo "  llama-index packages use Pydantic v1, which is incompatible with Python 3.14+"
            echo ""
            echo "  Solutions:"
            echo "  1. Use Python 3.13 or 3.12 (recommended):"
            echo "     brew install python@3.13"
            echo "     python3.13 -m venv .venv"
            echo "     source .venv/bin/activate"
            echo "     ./setup.sh"
            echo ""
            echo "  2. Or use pyenv to manage Python versions:"
            echo "     pyenv install 3.13.0"
            echo "     pyenv local 3.13.0"
            echo "     ./setup.sh"
            echo ""
            exit 1
        fi
        
        # Check minimum version (3.10+)
        if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 10 ]); then
            log_error "Python ${PYTHON_VERSION} is too old. LoBRA requires Python 3.10 or higher."
            echo "  Please upgrade Python: brew install python"
            exit 1
        fi
        
        log_success "Python ${PYTHON_VERSION} found"
    fi
    
    # Check Docker
    if ! command_exists docker; then
        missing_deps+=("docker")
    else
        if ! docker info >/dev/null 2>&1; then
            log_warning "Docker is installed but not running. Attempting to start Docker Desktop..."
            
            # Try to start Docker Desktop (macOS)
            if [[ "$OSTYPE" == "darwin"* ]]; then
                if [ -d "/Applications/Docker.app" ]; then
                    log_info "Starting Docker Desktop..."
                    open -a Docker
                    
                    # Wait for Docker to start (max 60 seconds)
                    log_info "Waiting for Docker to start (this may take 30-60 seconds)..."
                    docker_started=false
                    for i in {1..60}; do
                        if docker info >/dev/null 2>&1; then
                            docker_started=true
                            break
                        fi
                        sleep 1
                        
                        # Progress indicator every 5 seconds
                        if [ $((i % 5)) -eq 0 ]; then
                            echo -n "."
                        fi
                    done
                    echo ""  # New line after dots
                    
                    if [ "$docker_started" = true ]; then
                        log_success "Docker Desktop started successfully"
                    fi
                    
                    # Final check
                    if ! docker info >/dev/null 2>&1; then
                        log_error "Docker Desktop failed to start. Please start it manually and re-run setup."
                        echo ""
                        echo "  To start Docker Desktop manually:"
                        echo "    1. Open Applications folder"
                        echo "    2. Double-click Docker"
                        echo "    3. Wait for Docker icon in menu bar to show 'Docker Desktop is running'"
                        echo "    4. Then re-run: ./setup.sh"
                        exit 1
                    fi
                else
                    log_error "Docker Desktop not found. Please install Docker Desktop first."
                    exit 1
                fi
            else
                # Linux: try to start Docker service
                log_info "Attempting to start Docker service..."
                if command_exists systemctl; then
                    sudo systemctl start docker 2>/dev/null || true
                    sleep 2
                fi
                
                # Check again
                if ! docker info >/dev/null 2>&1; then
                    log_error "Docker is installed but not running. Please start Docker manually:"
                    echo "    sudo systemctl start docker"
                    exit 1
                fi
            fi
        fi
        log_success "Docker is installed and running"
    fi
    
    # Check Ollama
    if ! command_exists ollama; then
        missing_deps+=("ollama")
    else
        log_success "Ollama is installed"
    fi
    
    # Check Homebrew (macOS only)
    if [[ "$OSTYPE" == "darwin"* ]]; then
        if ! command_exists brew; then
            log_warning "Homebrew not found. Some dependencies may need manual installation."
        else
            log_success "Homebrew is installed"
        fi
    fi
    
    # Report missing dependencies
    if [ ${#missing_deps[@]} -gt 0 ]; then
        log_error "Missing required dependencies: ${missing_deps[*]}"
        echo ""
        echo "Please install missing dependencies:"
        echo ""
        for dep in "${missing_deps[@]}"; do
            case $dep in
                python3)
                    echo "  Python 3.10+:"
                    echo "    macOS: brew install python"
                    echo "    Linux: sudo apt install python3 python3-pip"
                    ;;
                docker)
                    echo "  Docker:"
                    echo "    macOS: brew install --cask docker"
                    echo "    Linux: Visit https://docs.docker.com/engine/install/"
                    ;;
                ollama)
                    echo "  Ollama:"
                    echo "    macOS: brew install ollama"
                    echo "    Linux: curl -fsSL https://ollama.com/install.sh | sh"
                    ;;
            esac
            echo ""
        done
        exit 1
    fi
    
    log_success "All prerequisites are met!"
}

# Setup Python virtual environment
setup_venv() {
    log_info "Setting up Python virtual environment..."
    
    if [ -d ".venv" ]; then
        log_warning "Virtual environment already exists. Skipping creation."
    else
        python3 -m venv .venv
        log_success "Virtual environment created at .venv"
    fi
    
    # Activate venv
    source .venv/bin/activate
    
    # Upgrade pip
    log_info "Upgrading pip..."
    pip install --upgrade pip >/dev/null 2>&1
    log_success "pip upgraded"
}

# Install Python dependencies
install_dependencies() {
    log_info "Installing Python dependencies (this may take a few minutes)..."
    
    source .venv/bin/activate
    
    if [ ! -f "requirements.txt" ]; then
        log_error "requirements.txt not found!"
        exit 1
    fi
    
    pip install -r requirements.txt
    log_success "Python dependencies installed"
    
    # Download NLTK data
    log_info "Downloading NLTK data..."
    python3 - <<'PY'
import nltk
import sys
try:
    nltk.download('punkt', quiet=True)
    nltk.download('punkt_tab', quiet=True)
    nltk.download('stopwords', quiet=True)
    print("NLTK data downloaded successfully")
except Exception as e:
    print(f"Warning: NLTK download issue: {e}", file=sys.stderr)
PY
    log_success "NLTK data downloaded"
}

# Start Ollama service
start_ollama() {
    log_info "Checking Ollama service..."
    
    # Check if Ollama is already running
    if curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
        log_success "Ollama service is already running"
        return 0
    fi
    
    # Try to start Ollama
    if [[ "$OSTYPE" == "darwin"* ]]; then
        log_info "Starting Ollama service..."
        brew services start ollama >/dev/null 2>&1 || {
            log_warning "Could not start Ollama via brew services, trying direct start..."
            nohup ollama serve > logs/ollama.log 2>&1 &
        }
        
        # Wait for Ollama to be ready
        log_info "Waiting for Ollama to be ready..."
        for i in {1..30}; do
            if curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
                log_success "Ollama service started"
                return 0
            fi
            sleep 1
        done
        
        log_error "Ollama service failed to start. Please run 'ollama serve' manually."
        exit 1
    else
        log_info "Please ensure Ollama service is running (run 'ollama serve' in another terminal)"
    fi
}

# Detect system memory and recommend models
detect_system_memory() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS - get total memory in GB
        TOTAL_MEM_BYTES=$(sysctl -n hw.memsize)
        TOTAL_MEM_GB=$((TOTAL_MEM_BYTES / 1024 / 1024 / 1024))
    else
        # Linux - get total memory in GB
        TOTAL_MEM_KB=$(grep MemTotal /proc/meminfo | awk '{print $2}')
        TOTAL_MEM_GB=$((TOTAL_MEM_KB / 1024 / 1024))
    fi
    
    echo "$TOTAL_MEM_GB"
}

# Pull Ollama models
pull_ollama_models() {
    log_info "Pulling Ollama models (this will take several minutes)..."
    
    # Check if Ollama is responding
    if ! curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
        log_error "Ollama service is not running. Please start it with 'ollama serve'"
        exit 1
    fi
    
    # Detect system memory
    TOTAL_MEM=$(detect_system_memory)
    log_info "Detected ${TOTAL_MEM}GB total system memory"
    
    # Read models from config.yaml
    source .venv/bin/activate
    CHAT_MODEL=$(python3 -c "import yaml; print(yaml.safe_load(open('config.yaml'))['chat_model'])")
    EMBED_MODEL=$(python3 -c "import yaml; print(yaml.safe_load(open('config.yaml'))['embed_model'])")
    
    # Show memory-appropriate recommendation
    if [ "$TOTAL_MEM" -le 8 ]; then
        log_info "💡 For 8GB RAM, using lightweight model: ${CHAT_MODEL}"
        echo ""
        echo "  Model sizes:"
        echo "    • llama3.2:3b  → ~2GB RAM (fast, efficient) ✓ Recommended"
        echo "    • phi3:mini    → ~2.3GB RAM (alternative)"
        echo "    • gemma2:2b    → ~1.6GB RAM (smallest)"
        echo ""
    elif [ "$TOTAL_MEM" -le 16 ]; then
        log_info "💡 For 16GB RAM, you can use: llama3.1:8b or ${CHAT_MODEL}"
    else
        log_info "💡 With ${TOTAL_MEM}GB RAM, you can use larger models if desired"
    fi
    
    log_info "Pulling chat model: ${CHAT_MODEL}..."
    ollama pull "${CHAT_MODEL}"
    log_success "Chat model pulled: ${CHAT_MODEL}"
    
    log_info "Pulling embedding model: ${EMBED_MODEL}..."
    ollama pull "${EMBED_MODEL}"
    log_success "Embedding model pulled: ${EMBED_MODEL}"
}

# Setup Qdrant vector database
setup_qdrant() {
    log_info "Setting up Qdrant vector database..."
    
    # Check if container already exists
    if docker ps -a --format '{{.Names}}' | grep -q "^qdrant$"; then
        log_warning "Qdrant container already exists"
        
        # Check if it's running
        if docker ps --format '{{.Names}}' | grep -q "^qdrant$"; then
            log_success "Qdrant is already running"
            return 0
        else
            log_info "Starting existing Qdrant container..."
            docker start qdrant
            log_success "Qdrant container started"
            return 0
        fi
    fi
    
    # Detect system memory for container limits
    TOTAL_MEM=$(detect_system_memory)
    
    # Create new container with appropriate memory limits
    log_info "Creating Qdrant container..."
    if [ "$TOTAL_MEM" -le 8 ]; then
        # For 8GB systems, limit Qdrant to 1GB
        log_info "Configuring Qdrant for 8GB system (1GB limit)..."
        docker run -d --name qdrant \
            -p 6333:6333 \
            -v qdrant_storage:/qdrant/storage \
            --memory="1g" \
            --memory-swap="1g" \
            qdrant/qdrant:latest
    else
        # For larger systems, use default (no limit)
        docker run -d --name qdrant \
            -p 6333:6333 \
            -v qdrant_storage:/qdrant/storage \
            qdrant/qdrant:latest
    fi
    
    # Wait for Qdrant to be ready
    log_info "Waiting for Qdrant to be ready..."
    for i in {1..30}; do
        if curl -s http://localhost:6333/health >/dev/null 2>&1; then
            log_success "Qdrant is running at http://localhost:6333"
            return 0
        fi
        sleep 1
    done
    
    log_error "Qdrant failed to start properly"
    exit 1
}

# Verify setup
verify_setup() {
    log_info "Verifying setup..."
    
    local errors=0
    
    # Check Python packages
    source .venv/bin/activate
    if ! python3 -c "import llama_index.core" 2>/dev/null; then
        log_error "llama-index-core not properly installed"
        errors=$((errors + 1))
    fi
    
    # Check Ollama
    if ! curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
        log_error "Ollama service is not responding"
        errors=$((errors + 1))
    fi
    
    # Check Qdrant
    if ! curl -s http://localhost:6333/health >/dev/null 2>&1; then
        log_error "Qdrant is not responding"
        errors=$((errors + 1))
    fi
    
    # Check vault directory
    if [ ! -d "vault" ]; then
        log_warning "vault/ directory not found, creating it..."
        mkdir -p vault
    fi
    
    if [ $errors -eq 0 ]; then
        log_success "All components verified successfully!"
        return 0
    else
        log_error "Setup verification failed with $errors error(s)"
        return 1
    fi
}

# Print usage instructions
print_usage() {
    TOTAL_MEM=$(detect_system_memory)
    
    echo ""
    echo "╔═══════════════════════════════════════════════════════╗"
    echo "║                  Setup Complete!                      ║"
    echo "╚═══════════════════════════════════════════════════════╝"
    echo ""
    
    # Hardware-specific message
    if [ "$TOTAL_MEM" -le 8 ]; then
        echo "🎯 ${GREEN}Optimized for your ${TOTAL_MEM}GB system!${NC}"
        echo ""
        echo "   Your configuration uses:"
        echo "   • llama3.2:3b (lightweight, fast)"
        echo "   • Memory-efficient settings"
        echo "   • Qdrant limited to 1GB RAM"
        echo ""
        echo "   ${YELLOW}📖 See 8GB-QUICKREF.md for tips specific to your hardware${NC}"
        echo ""
    fi
    
    echo "Next steps:"
    echo ""
    echo "  1. Activate the virtual environment:"
    echo "     ${GREEN}source .venv/bin/activate${NC}"
    echo ""
    echo "  2. Add your knowledge files to the vault/ directory:"
    echo "     - Markdown files (.md) with YAML front-matter"
    echo "     - PDFs (.pdf)"
    echo "     - Text files (.txt)"
    echo "     - Code files"
    echo ""
    echo "  3. Index your knowledge:"
    echo "     ${GREEN}make ingest${NC}"
    echo ""
    echo "  4. Ask questions:"
    echo "     ${GREEN}make ask q=\"your question here\"${NC}"
    echo ""
    echo "Example:"
    echo "  ${GREEN}make ask q=\"Summarize my notes on machine learning\"${NC}"
    echo ""
    echo "Useful commands:"
    echo "  ${BLUE}make clean${NC}        - Clean index and logs"
    echo "  ${BLUE}make verify${NC}       - Check system health"
    echo "  ${BLUE}docker logs qdrant${NC} - View Qdrant logs"
    echo "  ${BLUE}ollama list${NC}        - List installed models"
    echo ""
}

# Main setup flow
main() {
    print_banner
    
    # Change to script directory
    cd "$(dirname "$0")"
    
    # Run setup steps
    check_prerequisites
    setup_venv
    install_dependencies
    start_ollama
    pull_ollama_models
    setup_qdrant
    
    if verify_setup; then
        print_usage
        exit 0
    else
        log_error "Setup completed with errors. Please check the messages above."
        exit 1
    fi
}

# Run main function
main

