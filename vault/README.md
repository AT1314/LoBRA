---
title: "README"
date: "2025-10-29"
source: "inbox/README.md"
format: "Markdown"
processed: "2025-10-31 10:24:36"
---

# LoBRA Inbox

Drop files here for automatic conversion to markdown!

## How It Works

1. **Add files** to this folder:
   ```bash
   cp your-document.docx inbox/
   cp presentation.pptx inbox/
   cp data.xlsx inbox/
   ```

2. **Convert** to markdown:
   ```bash
   make pipeline
   ```

3. Files are **converted** to `vault/` and **originals moved** to `processed/`

## Supported Formats

✅ **Documents**
- Word (.docx, .doc)
- PDF (.pdf) - native support

✅ **Presentations**
- PowerPoint (.pptx, .ppt)

✅ **Data**
- Excel (.xlsx, .xls)
- CSV (.csv)

✅ **Web**
- HTML (.html, .htm)

✅ **Books**
- EPUB (.epub)

✅ **Images** (requires OCR setup)
- PNG, JPG, JPEG (.png, .jpg, .jpeg)

✅ **Text**
- Markdown (.md) - direct copy
- Plain text (.txt)

## Quick Start

```bash
# First time: Install converters
make install-pipeline

# Ongoing: Convert files
make pipeline

# Or: Auto-watch mode
make watch  # Converts every 5 seconds, Ctrl+C to stop
```

## Tips

- **Batch processing:** Add multiple files, then run `make pipeline` once
- **Organization:** Use subdirectories (e.g., `inbox/2025-10/`, `inbox/courses/`)
- **Large files:** On 8GB RAM, process 5-10 files at a time

## After Conversion

Files are automatically:
1. ✅ Converted to markdown with metadata
2. ✅ Saved to `vault/` (ready for indexing)
3. ✅ Originals moved to `processed/` (archived)

Then run:
```bash
make ingest  # Index new files
make ask q="your question"  # Query your knowledge
```

## Need Help?

- Quick guide: `PIPELINE-QUICKSTART.md`
- Full details: `PIPELINE.md`
- Main docs: `README.md`