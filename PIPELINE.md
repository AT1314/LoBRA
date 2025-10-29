# LoBRA Data Pipeline

Automatically convert Word, PowerPoint, Excel, HTML, EPUB, and images into markdown for your knowledge base.

## Quick Start

```bash
# 1. Install converters (one-time)
make install-pipeline

# 2. Add files
cp your-file.docx inbox/
cp presentation.pptx inbox/
cp data.xlsx inbox/

# 3. Convert
make pipeline

# 4. Index & query
make ingest
make ask q="your question"
```

**Supported formats:** Word, PowerPoint, Excel, CSV, HTML, EPUB, Images (OCR), PDF, Markdown

**Auto-watch mode:** `make watch` - automatically converts files as they arrive

---

## Daily Workflow

```bash
# Morning: Add yesterday's files
cp ~/Documents/meetings/*.pptx inbox/
cp ~/Desktop/*.docx inbox/

# Convert all
make pipeline

# Index
make ingest

# Query
make ask q="Summarize yesterday's meeting notes"
```

---

## Commands

| Command | Description |
|---------|-------------|
| `make install-pipeline` | Install format converters (one-time) |
| `make pipeline` | Convert all files from inbox/ to vault/ |
| `make watch` | Auto-convert new files continuously (Ctrl+C to stop) |

---

## Directory Structure

```
inbox/          →    vault/          →    brain/
(originals)          (markdown)           (indexed)
                          ↓
                     processed/
                   (archived originals)
```

**Workflow:**
1. Drop files in `inbox/`
2. Run `make pipeline` → converts to markdown in `vault/`
3. Originals moved to `processed/`
4. Run `make ingest` → indexes for search

---

## Supported Formats

### Documents
- **Word** (.docx, .doc) - Requires: `docx2txt`
- **PowerPoint** (.pptx, .ppt) - Requires: `python-pptx`
- **PDF** (.pdf) - Built-in support (no conversion needed)

### Data
- **Excel** (.xlsx, .xls) - Requires: `pandas`, `openpyxl`
- **CSV** (.csv) - Requires: `pandas`

### Web & Markup
- **HTML** (.html, .htm) - Requires: `html2text`
- **Markdown** (.md) - Direct copy (no conversion)

### Books
- **EPUB** (.epub) - Requires: `ebooklib`

### Images
- **Images** (.png, .jpg, .jpeg, .tiff) - Requires: `pytesseract`, `tesseract-ocr` (OCR)

---

## Installation

### Basic Setup (Recommended)

```bash
source .venv/bin/activate
make install-pipeline
```

Installs converters for Word, PowerPoint, Excel, HTML, EPUB (~50MB)

### With OCR Support (Optional)

```bash
# Python packages (already installed)
make install-pipeline

# System package for OCR
brew install tesseract  # macOS
sudo apt install tesseract-ocr  # Linux
```

---

## Usage Examples

### Single File

```bash
cp report.docx inbox/
make pipeline
```

### Batch Processing

```bash
cp ~/Documents/*.docx inbox/
cp ~/Documents/*.pptx inbox/
cp ~/Documents/*.xlsx inbox/
make pipeline
```

### Auto-Watch Mode

```bash
make watch
```

Drop files in `inbox/` - they convert automatically every 5 seconds.

---

## Output Format

All converted files include metadata:

```markdown
---
title: "My Document"
date: "2025-10-29"
source: "inbox/my-document.docx"
format: "Word Document"
converted: "2025-10-29 14:30:00"
---

# Content starts here...
```

**Add custom metadata:** Edit converted files in `vault/` to add tags, course, project, etc., then run `make ingest`.

---

## Performance (8GB M1 MacBook Air)

| File Type | Size | Time | Notes |
|-----------|------|------|-------|
| Word | 50KB | < 1s | Fast |
| PowerPoint | 2MB | 2-3s | Moderate |
| Excel | 500KB | 1-2s | Fast |
| HTML | 100KB | < 1s | Fast |
| EPUB | 5MB | 10-15s | Slower for large books |
| Image OCR | 2MB | 5-8s | Requires tesseract |

**Memory usage:** ~500MB-1GB during conversion

**For 8GB RAM:**
- Process 5-10 files at a time
- Large files (>10MB) may take longer
- Close other apps during batch conversion

---

## Format-Specific Tips

### Word Documents
**Best results:**
- Use heading styles (Heading 1, 2, 3)
- Clean formatting focuses on content

**Limitations:**
- Complex tables may not convert perfectly
- Images not extracted (text only)

### PowerPoint
**Best results:**
- Keep text in text boxes
- Simple layouts work best

**Limitations:**
- Images not extracted
- Animations ignored

### Excel/CSV
**Best results:**
- Clean, tabular data
- Use first row as headers

**Limitations:**
- Formulas converted to values
- Charts/graphs not captured

### HTML
**Best results:**
- Well-formed HTML
- Semantic markup

**Limitations:**
- JavaScript/CSS removed
- Complex layouts may break

### Images (OCR)
**Best results:**
- High resolution (300+ DPI)
- Clear printed text
- Good contrast

**Limitations:**
- Handwriting recognition poor
- May have OCR errors

### EPUB Books
**Best results:**
- Standard EPUB format
- Clear chapter structure

**Limitations:**
- DRM-protected EPUBs won't work
- Images not extracted

---

## Troubleshooting

### "No converter found for file"
**Solution:** File format not supported. Export as PDF or convert manually.

### "docx2txt not installed"
```bash
source .venv/bin/activate
pip install docx2txt
```

### "pytesseract not installed" (for OCR)
```bash
pip install pytesseract Pillow
brew install tesseract  # macOS
sudo apt install tesseract-ocr  # Linux
```

### "pandas not installed"
```bash
pip install pandas openpyxl xlrd tabulate
```

### "Out of memory" (8GB RAM)
**Solutions:**
1. Process files one at a time
2. Close other applications
3. Split large files into smaller parts

### Converted file is empty
**Possible causes:**
- Source file is empty or corrupted
- Format not fully supported
- Try re-exporting from original application

---

## Best Practices

### 1. Organize Your Inbox
```bash
# By date
inbox/2025-10-29/
  ├── lecture-notes.pptx
  └── reading.pdf

# By topic
inbox/machine-learning/
  ├── notes.docx
  └── paper.pdf
```

Pipeline processes subdirectories automatically!

### 2. Regular Processing
```bash
# Daily workflow
cp ~/Documents/today/*.* inbox/
make pipeline
make ingest
```

### 3. Archive Management
Originals are moved to `processed/`. Periodically clean up:
```bash
# Keep last 30 days
find processed -type f -mtime +30 -delete

# Or move to external storage
mv processed ~/Archive/lobra-processed-$(date +%Y%m)
```

### 4. Quality Check
After conversion, spot-check files:
```bash
cat vault/your-file.md | less
```

---

## Advanced Usage

### Processing Large Files

**Option 1:** Process individually
```bash
cp large-book.epub inbox/
make pipeline
# Wait before adding more
```

**Option 2:** Split large files
- Break documents into chapters
- Process separately
- Easier to query later

### Custom Metadata

Edit converted files in `vault/` to add:
```markdown
---
title: "Machine Learning Notes"
tags: [ml, deep-learning]
course: "CS229"
project: "ML-Research"
---
```

Then run `make ingest` to reindex.

### Extending the Pipeline

Add support for new formats by editing `scripts/preprocess.py`:

```python
class YourConverter(FileConverter):
    def __init__(self, config):
        super().__init__(config)
        self.supported_formats = ['.your', '.ext']
    
    def convert(self, input_path, output_path):
        # Your conversion logic
        pass
```

Register in `DataPipeline.__init__`:
```python
self.converters = [
    # ... existing converters ...
    YourConverter(self.config),
]
```

---

## Summary

The data pipeline makes it easy to add knowledge from any source:

1. 📥 **Drop files** in `inbox/`
2. 🔄 **Run** `make pipeline`
3. 📚 **Index** with `make ingest`
4. 💡 **Query** with `make ask q="your question"`

All your documents, presentations, spreadsheets, and more become searchable knowledge!

Need help? See `README.md` for general LoBRA documentation.
