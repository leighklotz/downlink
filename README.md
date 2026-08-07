# Downlink

[![GitHub Stars](https://img.shields.io/github/stars/leighklotz/downlink)](https://github.com/leighklotz/downlink)
[![GitHub License](https://img.shields.io/github/license/leighklotz/downlink)](https://github.com/leighklotz/downlink/blob/main/LICENSE)

Playwright-based CLI to render a webpage and convert its rendered HTML to Markdown.  Perfect for archiving, creating documentation, or simplifying web content.

## Features

*   **HTML to Markdown Conversion:**  Reliably converts rendered HTML into clean Markdown.
*   **Playwright Powered:**  Built on Playwright for accurate rendering, including JavaScript execution.
*   **Easy Installation:**  Simple one-step installation scripts provided via `pip` or `uv`.
*   **Drop Links Option:**  Removes hyperlinks and image links for a cleaner output.

## Quickstart (Installation)

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/leighklotz/downlink.git
    cd downlink
    ```

2.  **Run your preferred installer:**

    You can choose between a standard `pip` installation or a faster installation using `uv`. You must provide a directory where you want the `downlink` command to be symlinked (e.g., `~/.local/bin`).

    ### Option A: Standard Installation (`install-pip.sh`)
    Recommended if you want all Playwright browsers installed with their system dependencies automatically. This uses standard Python virtual environments.
    ```bash
    ./install-pip.sh ~/.local/bin
    ```
    or
    ```bash
    ./install.sh ./bin
    ```

    ### Option B: Fast Installation (`install-uv.sh`)
    Requires [`uv`](https://github.com/astral-sh/uv) to be installed on your system. This method is significantly faster, installs only Chromium for Playwright, and generates a `requirements.txt` file automatically.
    ```bash
    ./install-uv.sh ~/.local/bin
    ```

## Usage

Once installed, use `downlink` to convert a webpage to Markdown:

```bash
downlink https://example.com/page
```

This will print the Markdown output to your terminal. To save the output to a file:

```bash
downlink https://example.com/page > output.md
```

###  Drop Links

To remove hyperlinks and image links from the output, use the `--drop_links` flag:

```bash
downlink --drop_links https://example.com/page > output.md
```

## Developer Setup

If you plan to contribute or need an editable install for development:

1.  **Activate the virtual environment:**

    Using standard `pip`:
    ```bash
    source .venv/bin/activate
    ```
    Or using `uv` if that was your installation method:
    ```bash
    # If you used uv to set up, it is recommended to use uv for dev tasks
    uv pip install -e .
    ```

2.  **Install in editable mode:**

    ```bash
    pip install -e .
    ```

## Troubleshooting

*   **Playwright Browser Errors:** If you encounter errors related to browser binaries, ensure the installation script completed successfully. Re-running it can resolve missing browser installations. Ensure you have sufficient disk space.
*   **Virtual Environment Issues:** If you experience problems with the virtual environment, try deleting the `.venv` directory and re-running your chosen install script.

## License

This project is licensed under the [MIT License](LICENSE).

