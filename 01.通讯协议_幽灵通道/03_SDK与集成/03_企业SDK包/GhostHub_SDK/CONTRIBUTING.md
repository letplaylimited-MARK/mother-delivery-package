# Contributing to Ghost Hub SDK

Thank you for your interest in contributing to Ghost Hub SDK!

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Install development dependencies:
   ```bash
   pip install -e ".[all]"
   pip install pytest pytest-cov black flake8 mypy
   ```

## Development Workflow

### 1. Branch Naming
- Feature: `feature/your-feature-name`
- Bugfix: `bugfix/issue-description`
- Documentation: `docs/improvement-description`

### 2. Code Style
We use standard Python conventions with `black` for formatting:

```bash
black ghost_hub_sdk/
flake8 ghost_hub_sdk/
```

### 3. Type Checking
```bash
mypy ghost_hub_sdk/
```

### 4. Running Tests
```bash
pytest tests/ -v
pytest tests/ --cov=ghost_hub_sdk
```

## Pull Request Process

1. Ensure all tests pass
2. Update documentation if needed
3. Add entry to CHANGELOG.md
4. Request review from maintainers
5. Squash commits before merging

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Follow the project's coding conventions

## Questions?

- GitHub Issues: https://github.com/ghost-hub/sdk/issues
- Documentation: https://docs.ghosthub.dev

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
