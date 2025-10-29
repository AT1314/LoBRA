# Contributing to LoBRA

Thank you for your interest in contributing to LoBRA! This document provides guidelines for contributing to the project.

## Development Setup

1. Fork and clone the repository
2. Run the setup script:
   ```bash
   ./setup.sh
   ```
3. Activate the virtual environment:
   ```bash
   source .venv/bin/activate
   ```

## Project Structure

```
LoBRA/
├── scripts/          # Core functionality
│   ├── ingest.py    # Document processing and indexing
│   └── query.py     # Query processing and retrieval
├── vault/           # Example knowledge base
├── config.yaml      # Configuration file
├── setup.sh         # Automated setup script
├── verify.sh        # Environment verification
└── Makefile         # Common tasks
```

## Development Guidelines

### Code Style

- Follow PEP 8 for Python code
- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused and modular

### Adding Features

1. **Create a new branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Implement your feature**:
   - Add code with proper documentation
   - Update relevant configuration if needed
   - Test thoroughly

3. **Update documentation**:
   - Update README.md if needed
   - Add usage examples
   - Update QUICKSTART.md if it affects user workflow

4. **Submit a pull request**:
   - Describe what your feature does
   - Explain why it's useful
   - Include any breaking changes

### Areas for Contribution

#### High Priority
- [ ] Web UI (FastAPI/Streamlit)
- [ ] Incremental indexing (only re-process changed files)
- [ ] Better error handling and logging
- [ ] Unit tests

#### Medium Priority
- [ ] Cross-encoder reranking
- [ ] Metadata filtering in queries
- [ ] Multi-language support
- [ ] Export/import configurations

#### Nice to Have
- [ ] Conversation history
- [ ] Query suggestions
- [ ] Integration with note-taking apps
- [ ] Mobile app

### Testing

Currently, the project doesn't have automated tests. Contributions to add testing infrastructure are highly welcome!

**Manual Testing Checklist**:
1. Run `make ingest` with sample files
2. Test various query types
3. Verify citations are accurate
4. Check error handling

### Code Review Process

1. All contributions require review
2. Reviewers will check:
   - Code quality and style
   - Documentation completeness
   - Functionality and correctness
   - No breaking changes (or properly documented)

## Feature Requests

Have an idea? Open an issue with:
- Clear description of the feature
- Use case / motivation
- Proposed implementation (if you have one)

## Bug Reports

Found a bug? Open an issue with:
- Description of the bug
- Steps to reproduce
- Expected vs. actual behavior
- Your environment (OS, Python version, etc.)
- Relevant logs

## Questions

For questions:
- Check existing documentation first
- Search closed issues
- Open a new issue with the "question" label

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be acknowledged in:
- README.md
- Release notes

Thank you for helping make LoBRA better! 🎉

