# Contributing to Ghost Channel Protocol

Thank you for your interest in contributing to the Ghost Channel Protocol project!

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).

## How to Contribute

### Reporting Bugs

1. Check if the bug is already reported in [Issues](../../issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - SDK version and environment details

### Suggesting Features

1. Check existing issues for similar suggestions
2. Create a new issue with:
   - Clear use case description
   - Expected behavior
   - How it aligns with RFC 0001

### Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Run tests: `npm test` (TS) or `pytest` (Python)
5. Commit with clear messages
6. Push and open a Pull Request

## Development Setup

### Python SDK

```bash
cd python
pip install -e .
pytest tests/
```

### TypeScript SDK

```bash
cd typescript
npm install
npm test
```

## Style Guidelines

- Follow existing code style
- Add tests for new features
- Update documentation as needed
- Keep commits atomic

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
