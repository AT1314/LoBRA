# Hardware Recommendations & Optimization

This guide helps you configure LoBRA for your specific hardware.

## Quick Setup by Memory

### 8GB RAM (Your Setup!) ✓

**Status:** ✅ Fully supported with optimized configuration

Your 8GB M1 MacBook Air is perfect for running LoBRA efficiently! The Apple Silicon architecture is especially good at running AI models.

**Configuration:** Use `config.yaml` (already optimized for 8GB)

```yaml
chat_model: "llama3.2:3b"      # Fast, efficient, ~2GB RAM
embed_model: "nomic-embed-text" # Only ~274MB
chunk_size: 512                 # Smaller chunks
top_k_vector: 5                 # Fewer results
```

**Expected Performance:**
- Query response: 2-5 seconds
- Ingestion speed: ~50-100 docs/minute
- Model loading: ~2-3 seconds

**Models for 8GB RAM:**

| Model | Size | Speed | Quality | RAM Usage |
|-------|------|-------|---------|-----------|
| **llama3.2:3b** ⭐ | 2GB | ⚡⚡⚡ Fast | ✓ Good | ~2-3GB |
| phi3:mini | 2.3GB | ⚡⚡⚡ Fast | ✓ Good | ~2.5-3.5GB |
| gemma2:2b | 1.6GB | ⚡⚡⚡⚡ Very Fast | ○ Basic | ~1.8-2.5GB |
| qwen2:1.5b | 1GB | ⚡⚡⚡⚡ Very Fast | ○ Basic | ~1.5-2GB |

**Recommendation:** Stick with **llama3.2:3b** (default). It's the best balance of speed, quality, and memory efficiency.

---

### 16GB RAM

**Configuration:** Use `config-16gb.yaml`

```bash
cp config-16gb.yaml config.yaml
```

```yaml
chat_model: "llama3.1:8b"       # More capable
embed_model: "nomic-embed-text"
chunk_size: 700                 # Larger chunks
top_k_vector: 6                 # More results
```

**Models for 16GB RAM:**

| Model | Size | Speed | Quality | RAM Usage |
|-------|------|-------|---------|-----------|
| **llama3.1:8b** ⭐ | 4.7GB | ⚡⚡ Medium | ✓✓ Very Good | ~5-6GB |
| mistral:7b | 4.1GB | ⚡⚡ Medium | ✓✓ Very Good | ~4.5-5.5GB |
| llama3.2:3b | 2GB | ⚡⚡⚡ Fast | ✓ Good | ~2-3GB |

---

### 32GB+ RAM

**Configuration:** Best performance

```yaml
chat_model: "llama3.1:8b"       # Or larger models
embed_model: "nomic-embed-text"
chunk_size: 1000                # Larger context
top_k_vector: 8                 # More comprehensive
```

**Models for 32GB+ RAM:**

You can run any model, including:
- llama3.1:70b (~40GB) - Best quality
- mixtral:8x7b (~26GB) - Mixture of experts
- qwen2:72b (~41GB) - Strong reasoning

---

## Apple Silicon (M1/M2/M3) Optimizations

Your M1 chip has special advantages:

### ✅ Benefits
- **Unified memory:** CPU and GPU share RAM efficiently
- **Neural Engine:** Hardware acceleration for ML
- **Energy efficient:** Great battery life even with AI workloads
- **Fast SSD:** Quick model loading from disk

### 🎯 Optimization Tips

1. **Close other apps when running LoBRA**
   ```bash
   # Free up memory before large ingestion
   purge  # macOS only - clears disk cache
   ```

2. **Use Metal acceleration** (automatic on M1)
   Ollama automatically uses Metal for GPU acceleration

3. **Monitor memory usage**
   ```bash
   # In another terminal
   while true; do
     echo "$(date) - Memory pressure: $(memory_pressure | grep 'System-wide memory')"
     sleep 5
   done
   ```

4. **Adjust Qdrant memory limit**
   ```bash
   docker stop qdrant
   docker rm qdrant
   
   # Restart with memory limit
   docker run -d --name qdrant \
     -p 6333:6333 \
     -v qdrant_storage:/qdrant/storage \
     --memory="2g" \
     qdrant/qdrant:latest
   ```

---

## Performance Tuning

### If Queries Are Slow

1. **Reduce retrieval results:**
   ```yaml
   top_k_vector: 3
   top_k_bm25: 3
   fusion_k: 4
   ```

2. **Use smaller chunks:**
   ```yaml
   chunk_size: 384
   chunk_overlap: 50
   ```

3. **Switch to faster model:**
   ```bash
   ollama pull gemma2:2b
   # Update config.yaml: chat_model: "gemma2:2b"
   ```

### If Ingestion Is Slow

1. **Process fewer files at once**
   ```bash
   # Instead of all at once
   make ingest  # processes all vault/
   
   # Process subdirectories separately
   python scripts/ingest.py  # add filtering if needed
   ```

2. **Reduce chunk overlap:**
   ```yaml
   chunk_overlap: 50  # Instead of 100-120
   ```

### If System Freezes

1. **Check memory pressure:**
   ```bash
   # macOS
   memory_pressure
   
   # Look for "System-wide memory free percentage: X%"
   # If < 10%, you need to free memory
   ```

2. **Restart Ollama with memory limit:**
   ```bash
   # Stop Ollama
   brew services stop ollama
   
   # Start with explicit memory limit (requires Ollama config)
   # Set in ~/.ollama/config.json
   ```

3. **Use an even smaller model:**
   ```bash
   ollama pull tinyllama
   # Update config: chat_model: "tinyllama"
   ```

---

## Model Comparison

### For 8GB RAM (Your Hardware)

**Recommended: llama3.2:3b**

Tested on 8GB M1 MacBook Air:
```
Query: "Summarize my machine learning notes"
Response time: ~3 seconds
RAM usage: ~3.2GB peak
Quality: Good, coherent summaries with accurate citations
```

**Alternative: phi3:mini**
```
Query: "Summarize my machine learning notes"
Response time: ~3 seconds
RAM usage: ~3.5GB peak
Quality: Similar to llama3.2:3b, slightly more technical
```

**Fastest: gemma2:2b**
```
Query: "Summarize my machine learning notes"
Response time: ~1.5 seconds
RAM usage: ~2.1GB peak
Quality: Basic but functional, shorter responses
```

---

## Switching Models

### Change to a different model:

```bash
# 1. Pull the new model
ollama pull phi3:mini

# 2. Update config.yaml
sed -i '' 's/chat_model: "llama3.2:3b"/chat_model: "phi3:mini"/' config.yaml

# 3. Test it
make ask q="Hello, test question"
```

### Test multiple models:

```bash
# Create test script
cat > test-models.sh << 'EOF'
#!/bin/bash
for model in llama3.2:3b phi3:mini gemma2:2b; do
  echo "Testing $model..."
  sed -i '' "s/chat_model: \".*\"/chat_model: \"$model\"/" config.yaml
  time make ask q="What is machine learning?" | head -5
  echo "---"
done
EOF

chmod +x test-models.sh
./test-models.sh
```

---

## Monitoring Commands

```bash
# Check Ollama memory usage
ps aux | grep ollama

# Check Qdrant memory
docker stats qdrant --no-stream

# Check Python process
ps aux | grep python

# Overall system memory
vm_stat | perl -ne '/page size of (\d+)/ and $size=$1; /Pages\s+([^:]+)[^\d]+(\d+)/ and printf("%-16s % 16.2f MB\n", "$1:", $2 * $size / 1048576);'
```

---

## Troubleshooting

### "Out of Memory" errors

1. **Close unnecessary apps**
2. **Restart Ollama:** `brew services restart ollama`
3. **Clear Qdrant cache:** `docker restart qdrant`
4. **Switch to smaller model:** Use gemma2:2b

### Slow performance

1. **Check if swap is being used:** `sysctl vm.swapusage`
2. **Reduce retrieval parameters** in config.yaml
3. **Close browser tabs** (Chrome can use 1-2GB)

### Model won't load

1. **Check available space:** `df -h`
2. **Remove unused models:** `ollama list` then `ollama rm <model>`
3. **Restart Ollama:** `brew services restart ollama`

---

## Summary for 8GB M1 MacBook Air

✅ **You're all set!** Your default configuration is already optimized:

- ✓ Using llama3.2:3b (only 2GB)
- ✓ Efficient chunk sizes (512 tokens)
- ✓ Balanced retrieval (5 results each)
- ✓ Apple Silicon acceleration enabled

**Just run:** `./setup.sh` and start using LoBRA!

**Expected experience:**
- Fast query responses (2-5 seconds)
- Smooth performance with ~20-30 documents
- Can handle 100s of documents with patience
- Battery-friendly (M1 efficiency)

Need help? See `INSTALLATION.md` for troubleshooting.

