#!/usr/bin/env python3
"""
Safe ingestion for 8GB RAM - process just 2-3 documents at a time
This avoids overwhelming Ollama
"""

import sys
import shutil
from pathlib import Path

VAULT = Path("vault")
BACKUP_DIR = Path("vault-backup")

print("="*60)
print("SAFE INGESTION - Process 2-3 documents at a time")
print("="*60)

# Step 1: Backup all files
if not BACKUP_DIR.exists():
    print("\n1. Backing up all files...")
    BACKUP_DIR.mkdir()
    for f in VAULT.glob("*.md"):
        shutil.copy(f, BACKUP_DIR / f.name)
    print(f"   ✓ Backed up {len(list(BACKUP_DIR.glob('*.md')))} files")

# Step 2: Get list of files to process
backup_files = list(BACKUP_DIR.glob("*.md"))
if not backup_files:
    print("\nNo files in backup! Run ingestion normally first.")
    sys.exit(1)

print(f"\n2. Found {len(backup_files)} files total")
print("\n3. Processing strategy:")
print("   - Keep only 2-3 files in vault/ at a time")
print("   - Run make ingest-incremental")
print("   - Add more files gradually")

response = input("\nStart processing? (y/n): ")
if response.lower() != 'y':
    sys.exit(0)

# Process in small batches
BATCH_SIZE = 2
processed = 0

for i in range(0, len(backup_files), BATCH_SIZE):
    batch = backup_files[i:i + BATCH_SIZE]
    batch_num = i // BATCH_SIZE + 1
    
    print(f"\n{'='*60}")
    print(f"BATCH {batch_num} - Processing {len(batch)} files")
    print(f"{'='*60}")
    
    # Clear vault and add batch
    print("\n1. Setting up batch...")
    for f in VAULT.glob("*.md"):
        f.unlink()
    
    for f in batch:
        shutil.copy(f, VAULT / f.name)
        print(f"   ✓ Added: {f.name}")
    
    print(f"\n2. Run this command:")
    print(f"   make ingest-incremental")
    print(f"\n   Or:")
    print(f"   python scripts/ingest-incremental.py")
    
    response = input(f"\n✓ Press Enter after batch {batch_num} completes, or 'q' to quit: ")
    if response.lower() == 'q':
        break
    
    processed += len(batch)
    print(f"\n✓ Batch {batch_num} done! ({processed}/{len(backup_files)} files processed)")

print(f"\n{'='*60}")
print(f"Completed: {processed}/{len(backup_files)} files")
print(f"{'='*60}")

