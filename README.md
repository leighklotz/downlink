# Downlink

[![GitHub Stars](https://img.shields.io/github/stars/leighklotz/downlink)](https://github.com/leighklotz/downlink)
[![GitHub License](https://img.shields.io/github/license/leighklotz/downlink)](https://github.com/leighklotz/downlink/blob/main/LICENSE)

Playwright-based CLI to render a webpage and convert its rendered HTML to Markdown.  Perfect for archiving, creating documentation, or simplifying web content.

## Features

*   **HTML to Markdown Conversion:**  Reliably converts rendered HTML into clean Markdown.
*   **Playwright Powered:**  Built on Playwright for accurate rendering, including JavaScript execution.
*   **Easy Installation:**  Simple one-step installation script.
*   **Drop Links Option:** Removes hyperlinks and image links for a cleaner output.

## Quickstart (One-Step Installer)

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/leighklotz/downlink.git
    cd downlink
    ```

2.  **Run the installer:**

    ```bash
    ./install.sh ~/.local/bin
    ```

    This script:

    *   Creates a virtual environment (`.venv`)
    *   Activates the virtual environment
    *   Upgrades `pip`, `setuptools`, and `wheel`
    *   Installs `downlink` locally (`pip install .`)
    *   Downloads and installs necessary Playwright browser binaries (`python -m playwright install`)

## Usage

Once installed, use `downlink` to convert a webpage to Markdown:

```bash
downlink https://example.com/page
```

This will print the Markdown output to your terminal.  To save the output to a file:

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

    ```bash
    source .venv/bin/activate
    ```

2.  **Install in editable mode:**

    ```bash
    pip install -e .
    ```

## Troubleshooting

*   **Playwright Browser Errors:** If you encounter errors related to browser binaries, ensure the `install.sh` script completed successfully. Re-running it can resolve missing browser installations. Ensure you have sufficient disk space.
*   **Virtual Environment Issues:** If you experience problems with the virtual environment, try deleting the `.venv` directory and re-running `install.sh`.

## License

This project is licensed under the [MIT License](LICENSE).
```
