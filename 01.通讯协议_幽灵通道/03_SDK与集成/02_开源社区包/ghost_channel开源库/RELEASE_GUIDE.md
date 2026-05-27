# GitHub & PyPI Release Guide

## Step 1: Install GitHub CLI

```powershell
# Windows
winget install GitHub.cli

# Or download from: https://cli.github.com/
```

## Step 2: Authenticate

```bash
gh auth login
```

## Step 3: Create GitHub Repository

```bash
cd open-source
gh repo create q-spectrum/ghost-channel --public --source=. --push
```

## Step 4: Create Initial Commit

```bash
cd open-source
git add .
git commit -m "v1.0.0: Initial open source release

Features:
- Delta sync (61-93% bandwidth reduction)
- Vector clocks (100% causal consistency)
- AES-256-GCM encryption
- Merkle verification
- Audit logging

MIT License with competition restriction clause."
git push -u origin main
git tag v1.0.0
git push origin v1.0.0
```

## Step 5: Create GitHub Release

```bash
gh release create v1.0.0 \
  --title "Ghost Channel v1.0.0" \
  --notes "First open source release!

## Features
- Delta sync engine (61-93% bandwidth reduction)
- Vector clocks (100% causal consistency)
- AES-256-GCM encryption
- Merkle tree verification
- Complete audit trail

## License
MIT License - See LICENSE for terms and restrictions."
```

## Step 6: Publish to PyPI

### Install build tools

```bash
pip install build twine
```

### Build the package

```bash
cd open-source
python -m build
```

### Upload to PyPI

```bash
# Test PyPI first (optional)
twine upload --repository testpypi dist/*

# Production PyPI
twine upload dist/*
```

## Step 7: Verify Release

- Check GitHub: https://github.com/q-spectrum/ghost-channel
- Check PyPI: https://pypi.org/project/ghost-channel/

## Quick Commands Summary

```bash
# Full release script
cd open-source
git add .
git commit -m "v1.0.0: Initial release"
git push
git tag v1.0.0
git push origin v1.0.0
gh release create v1.0.0 --title "v1.0.0"
python -m build
twine upload dist/*
```

---

## Troubleshooting

### PyPI Authentication Error
```bash
# Create API token at https://pypi.org/manage/account/token/
twine upload dist/* -u __token__ -p pypi-xxxxx
```

### GitHub Push Error
```bash
gh auth refresh
git push --force-with-lease
```
