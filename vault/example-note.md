---
title: "Getting Started with LoBRA"
date: 2025-10-29
tags: [rag, knowledge-management, tutorial]
project: "LoBRA"
summary: "Introduction to using LoBRA local brain assistant"
---

# Getting Started with LoBRA

## What is LoBRA?

LoBRA (Local Brain Assistant) is a local RAG system that helps you manage and query your personal knowledge base. It combines the power of:

- **Semantic search** using embeddings
- **Keyword search** using BM25
- **Local AI models** via Ollama (no API keys needed!)

## Key Features

### Privacy-First Design
All your data stays on your machine. No cloud services, no API calls to external servers.

### Hybrid Retrieval
LoBRA uses both semantic embeddings and keyword matching to find the most relevant information:

- **Embeddings** understand meaning and context
- **BM25** excels at exact keyword matching
- **RRF fusion** combines both for optimal results

### Source Citations
Every answer includes file path citations so you can verify the sources.

## How to Use

### 1. Add Knowledge
Simply drop your files into the `vault/` directory:
- Markdown files with YAML front-matter
- PDFs (research papers, textbooks)
- Code snippets
- Text files

### 2. Index
Run `make ingest` to process and index your files.

### 3. Query
Ask questions with `make ask q="your question"`.

## Best Practices

### Use YAML Front-Matter
Add metadata to your Markdown files for better organization:

```yaml
---
title: "Your Title"
date: 2025-10-29
tags: [tag1, tag2]
course: CSE101
project: "Project Name"
summary: "Brief description"
---
```

### Organize by Topics
Create subdirectories in `vault/` to organize by course, project, or topic:

```
vault/
├── cs229-ml/
├── research-papers/
└── code-snippets/
```

### Keep Notes Atomic
Break large topics into smaller, focused notes for better retrieval.

## Example Queries

- "Summarize my notes on neural networks"
- "What are the key points from the transformer paper?"
- "Show me code examples of binary search"
- "What did I learn about KV cache optimization?"

## Tips

- **Re-index after changes**: Run `make ingest` when you add or update files
- **Use specific questions**: More specific queries get better answers
- **Check citations**: Always verify the sources in the response

## Technical Details

LoBRA uses:
- **LlamaIndex** for RAG orchestration
- **Qdrant** for vector storage
- **Ollama** for local AI models (llama3.1:8b, nomic-embed-text)
- **Python 3.10+** for scripting

Happy knowledge management! 🧠

