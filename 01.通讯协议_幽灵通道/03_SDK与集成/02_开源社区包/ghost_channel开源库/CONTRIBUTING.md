# Contributing to Ghost Channel Protocol

Thank you for your interest in contributing!

## Development Setup

```bash
# Clone the repository
git clone https://github.com/q-spectrum/ghost-channel.git
cd ghost-channel

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest tests/unit -v
```

## Code Style

- Follow PEP 8
- Use type hints where possible
- Maximum line length: 100 characters
- Run black and isort before committing

```bash
black src/
isort src/
```

## Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Aim for 80% code coverage

```bash
pytest tests/ -v --cov=ghost_channel
```

## Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes with clear commit messages
4. Push to your branch
5. Open a Pull Request

## Issues

- Use GitHub Issues for bug reports and feature requests
- Include Python version and relevant environment details
- For bugs, provide minimal reproducible examples

## License

By contributing, you agree that your contributions will be licensed under the MIT License with the additional restriction that it cannot be used for commercial AI agent services competing with Q-SpecTrum.
