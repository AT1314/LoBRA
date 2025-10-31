# Troubleshooting Guide

## Ingestion Issues (Ollama Crashes)

### Symptom: "EOF (status code: 500)" during ingestion

**This usually means Ollama is running out of memory on 8GB systems.**

⚠️ **If failures happen frequently (every few batches), this is NOT normal.** Your system may not have enough free memory. Try the "Safe Mode" solution below.

### Solutions (in order):

#### 1. Restart Ollama
```bash
brew services restart ollama
# Wait 5 seconds, then retry
make ingest
```

#### 2. Clear Existing Index and Start Fresh

If ingestion keeps failing, clear the corrupted index:

```bash
# Edit scripts/ingest.py, uncomment lines 107-110:
# if collection_exists:
#     print(f"   Clearing existing collection '{COLL}' due to previous errors...")
#     client.delete_collection(COLL)
#     collection_exists = False

# Then run
make ingest
```

Or manually clear:
```bash
python3 -c "
from qdrant_client import QdrantClient
client = QdrantClient(url='http://localhost:6333')
client.delete_collection('local_brain')
print('Collection cleared')
"
```

#### 3. Process Fewer Documents

Instead of ingesting all files at once:

```bash
# Move most files out temporarily
mkdir vault-backup
mv vault/*.md vault-backup/
# Keep just 5-10 files
cp vault-backup/file1.md vault/
cp vault-backup/file2.md vault/
make ingest

# If successful, add more gradually
```

#### 4. Reduce Batch Size Further

Edit `scripts/ingest.py`, line 107:
```python
BATCH_SIZE = 3  # Even smaller
```

#### 5. Close Other Applications

On 8GB RAM:
- Close Chrome/Safari (saves 1-2GB)
- Close Slack/Discord
- Close other heavy apps
- Then retry ingestion

#### 6. Use Ollama with Lower Memory

Set environment variable before starting:
```bash
OLLAMA_NUM_GPU=0  # Don't use GPU (use CPU only, less memory)
ollama serve
```

#### 7. Process One Document at a Time

Create a simple script:
```bash
# process-one.sh
#!/bin/bash
for file in vault/*.md; do
  echo "Processing $file..."
  mkdir -p vault-single
  cp "$file" vault-single/
  cp config.yaml config-single.yaml
  # Edit config-single.yaml: vault_path: "./vault-single"
  # Then run ingest with that config
  # Move file back after success
done
```

---

## Query Issues

### "Ollama not responding"

```bash
# Check status
curl http://localhost:11434/api/tags

# Restart
brew services restart ollama
```

### "Qdrant connection error"

```bash
# Check if running
docker ps | grep qdrant

# Start if needed
docker start qdrant
```

---

## Pipeline Conversion Issues

### "No converter found"

File format not supported. Options:
1. Export to PDF (native support)
2. Export to Markdown manually
3. Copy text content to markdown

### "Out of memory during conversion"

On 8GB RAM:
- Process 5-10 files at a time
- Close other applications
- For large PDFs (>10MB), split manually

---

## General Memory Management (8GB RAM)

### Before Large Operations

```bash
# Close unnecessary apps
# Check memory
memory_pressure  # macOS

# Clear disk cache (macOS)
sudo purge

# Then run operation
```

### Monitor Memory During Ingestion

In another terminal:
```bash
watch -n 2 'ps aux | grep -E "ollama|python.*ingest" | grep -v grep'
```

---

## Still Having Issues?

1. **Check logs:**
   ```bash
   tail -f logs/*.log  # If logs exist
   docker logs qdrant  # Qdrant logs
   ```

2. **Verify all services:**
   ```bash
   make verify
   ```

3. **Full reset:**
   ```bash
   # Stop services
   brew services stop ollama
   docker stop qdrant
   
   # Clear data
   rm -rf brain/*
   docker rm qdrant
   
   # Restart
   brew services start ollama
   docker run -d --name qdrant -p 6333:6333 -v qdrant_storage:/qdrant/storage --memory="1g" qdrant/qdrant:latest
   
   # Try again with fewer documents
   ```

---

## Performance Tips for 8GB RAM

1. **Ingest incrementally** - Add 10-20 files at a time
2. **Close apps during ingestion** - Saves 1-2GB
3. **Use smaller batch sizes** - Already optimized (BATCH_SIZE=5)
4. **Restart Ollama before large jobs** - Fresh memory state
5. **Process during low-usage times** - Better system stability

---

## Contact & Resources

- Check `README.md` for general documentation
- See `HARDWARE.md` for 8GB optimization guide
- See `PIPELINE.md` for conversion issues

