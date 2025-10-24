# downlink

Simple CLI to download files using HTTP(S) with a progress bar.

Quick usage (pip-installable package)

1. Clone:
```bash
git clone <repo-url>
cd <repo-directory>
```

2. Create a virtual environment and install the package locally:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install .
```

You can also install in editable/development mode:
```bash
pip install -e .
```

3. Run the CLI:
```bash
# download a single file
downlink https://example.com/file.zip

# download multiple files into a directory
downlink -d downloads https://example.com/file1 https://example.com/file2

# save a single URL to a specific filename
downlink -o myfile.bin https://example.com/file.bin

# suppress progress output (still prints saved path)
downlink -q https://example.com/file.zip
```

Notes
- The project provides a console script entry point `downlink` via setuptools/pyproject.toml.
- Dependencies are `requests` and `tqdm`.
- If you'd like automated CI, packaging to PyPI, or additional features (resuming, retries, auth), I can add them.