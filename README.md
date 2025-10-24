````markdown
# downlink

Playwright-based CLI to render a webpage and convert its rendered HTML to Markdown.

Quickstart

1. Clone the repo:
```bash
git clone https://github.com/leighklotz/downlink.git
cd downlink
```

2. Create a virtual environment and install the package:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install .
```

3. Install Playwright browser binaries:
```bash
python -m playwright install
```

4. Run:
```bash
# Convert a page to markdown and print to stdout
downlink https://example.com/page

# Or use the module directly
python -m downlink.cli https://example.com/page
```

Notes
- The implementation uses Playwright to render client-side JS and markdownify to convert HTML to Markdown.
- Playwright requires an extra step to install browser binaries (`python -m playwright install`). See https://playwright.dev/python/.
````
