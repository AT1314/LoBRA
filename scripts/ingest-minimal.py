#!/usr/bin/env python3
"""
Minimal ingestion - process just a few documents to test
Usage: python scripts/ingest-minimal.py [num_files]
"""

import sys
import yaml
from pathlib import Path

# Load config
CFG = yaml.safe_load(open("config.yaml"))
VAULT = Path(CFG["vault_path"])

# Get number of files to process (default: 3)
num_files = int(sys.argv[1]) if len(sys.argv) > 1 else 3

print("="*60)
print("MINIMAL INGESTION TEST")
print("="*60)
print(f"\nThis will process only {num_files} files to test if Ollama is stable.")
print("If this works, you can gradually increase the number.\n")

# List available files
files = list(VAULT.glob("*.md"))
if not files:
    print("No .md files found in vault/")
    sys.exit(1)

print(f"Found {len(files)} files in vault/")
print(f"\nProcessing first {num_files} files:")
for i, f in enumerate(files[:num_files], 1):
    print(f"  {i}. {f.name}")

response = input("\nContinue? (y/n): ")
if response.lower() != 'y':
    print("Cancelled.")
    sys.exit(0)

# Create temporary vault with just these files
import shutil
import tempfile

temp_vault = Path(tempfile.mkdtemp()) / "vault"
temp_vault.mkdir()

print(f"\nCopying {num_files} files to temporary location...")
for f in files[:num_files]:
    shutil.copy(f, temp_vault / f.name)
    print(f"  ✓ {f.name}")

# Temporarily modify config
import json
original_config = yaml.safe_load(open("config.yaml"))
temp_config = original_config.copy()
temp_config['vault_path'] = str(temp_vault)

# Save temp config
with open('config-temp.yaml', 'w') as f:
    yaml.dump(temp_config, f)

print(f"\n{'='*60}")
print("Now run ingestion with this command:")
print(f"{'='*60}")
print("\npython3 << 'EOF'")
print("import yaml")
print("CFG = yaml.safe_load(open('config-temp.yaml'))")
print("# Modify scripts/ingest-incremental.py to use CFG")
print("# Or manually set VAULT path")
print("EOF")
print("\nOr modify config.yaml temporarily:")
print(f"  vault_path: \"{temp_vault}\"")
print("  Then run: make ingest-incremental")
print("\nAfter testing, restore config.yaml and remove temp files.")

