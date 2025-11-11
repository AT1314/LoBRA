# Incremental Ingestion Guide

## Overview

LoBRA now supports **smart incremental ingestion** that only processes new or modified files, saving time and resources.

## How It Works

The system tracks processed files in `brain/processed_files.json` using:
- File modification time
- File size

When you run `make ingest`, it:
1. Loads tracking data from previous runs
2. Scans `vault/` for files
3. Compares each file against tracking data
4. Only processes files that are:
   - **New** (not in tracking data)
   - **Modified** (modification time or size changed)

## Usage

### Default (Incremental)

```bash
make ingest
```

This is now the **default behavior**. It will:
- Skip already-processed files
- Only index new or modified documents
- Show summary of what was processed

Example output:
```
==> Scanning for new or modified documents...
   Previously processed: 37 files
   ✓ No new or modified documents found. Everything is up to date!
```

Or when there are changes:
```
==> Scanning for new or modified documents...
   Found 5 documents to process:
     • New: 3 files
     • Modified: 2 files
```

### Full Re-indexing

If you need to reprocess **everything** (e.g., after changing chunk size or embedding model):

```bash
make ingest-full
```

This uses the original `ingest.py` script that processes all files.

### Reset Tracking

To reset and start fresh:

```bash
rm brain/processed_files.json
make ingest
```

## Benefits

1. **⚡ Faster**: Only processes what changed
2. **💾 Efficient**: Saves computational resources
3. **🔄 Automatic**: No manual tracking needed
4. **📊 Transparent**: Shows what's being processed

## File Tracking

The tracking file `brain/processed_files.json` stores:
- File paths
- Modification signatures (timestamp + size)

Example:
```json
{
  "vault/example-note.md": "1699123456_2048",
  "vault/research-paper.pdf": "1699123789_524288"
}
```

## When to Use Full Re-indexing

Use `make ingest-full` when you've changed:
- Chunk size (`chunk_size` in `config.yaml`)
- Chunk overlap (`chunk_overlap` in `config.yaml`)
- Embedding model (`embed_model` in `config.yaml`)
- Want to completely rebuild the index

## Configuration Files Affected

- **`config.yaml`**: Your main configuration
- **`config-*.yaml`**: Preset configurations
- **`Makefile`**: Commands updated
  - `make ingest` → Smart incremental (default)
  - `make ingest-full` → Process everything
  - `make ingest-incremental` → Old incremental script (slower)

## Troubleshooting

### "Everything is up to date" but index seems incomplete

1. Check if the index exists:
   ```bash
   curl http://localhost:6333/collections/local_brain
   ```

2. If needed, reset and rebuild:
   ```bash
   rm brain/processed_files.json
   make ingest
   ```

### Want to reprocess specific files

1. Remove them from tracking:
   ```bash
   # Edit brain/processed_files.json and remove specific file entries
   ```

2. Or modify the file to trigger reprocessing:
   ```bash
   touch vault/your-file.md
   make ingest
   ```

### Tracking file corrupted

Simply delete and regenerate:
```bash
rm brain/processed_files.json
make ingest-full  # Rebuild everything with tracking
```

## Performance Comparison

### Before (Full Reindex)
- Processes all 37 files every time
- Takes ~10-15 minutes
- Reprocesses unchanged content

### After (Incremental)
- First run: Same as before (~10-15 minutes)
- Subsequent runs with no changes: **< 1 second**
- Adding 1 new file: **~30 seconds**
- Modifying 3 files: **~2-3 minutes**

## Technical Details

**Script**: `scripts/ingest-smart.py`

**Tracking file**: `brain/processed_files.json`

**Signature format**: `{modification_time}_{file_size}`

**Supported file types**:
- Markdown (`.md`, `.markdown`)
- PDF (`.pdf`)
- Text (`.txt`)

The script automatically:
- Creates tracking file on first run
- Updates tracking after successful indexing
- Handles errors gracefully
- Preserves existing index data

