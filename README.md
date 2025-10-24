# downlink

Playwright-based CLI to render a webpage and convert its rendered HTML to Markdown.

Quickstart (one-step installer)

1. Clone the repo:
```bash
git clone https://github.com/leighklotz/downlink.git
cd downlink
```

2. Make the installer executable and run it:
```bash
chmod +x install.sh
./install.sh
```

What install.sh does
- creates a .venv virtual environment
- activates it
- upgrades pip/setuptools/wheel
- installs the package locally (pip install .)
- runs Playwright browser installation (python -m playwright install, preferring --with-deps when available)

After the script completes the venv is created and Playwright browsers are installed. To re-enter the environment later:
```bash
source .venv/bin/activate
```

Run the CLI:
```bash
downlink https://example.com/page
```

Developer notes
- Playwright requires browser binaries; install.sh runs the install step automatically.
- If you prefer editable installs for development:
```bash
source .venv/bin/activate
pip install -e .
```
