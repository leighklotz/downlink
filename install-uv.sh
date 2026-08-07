#!/usr/bin/env bash
set -eu

SCRIPT_DIR="$(dirname "$(realpath "${BASH_SOURCE}")")"

BINDIR=$1

if [ -z "$BINDIR" ] ; then
    echo "specify BINDIR"
    exit 1
fi

# Check if $bindir/downlink exists and error out if it does.
if [ -e "${BINDIR}/downlink" ]; then
    echo "Error: ${BINDIR}/downlink already exists."
    exit 1
fi

VENV_DIR=".venv"

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "Error: 'uv' is not installed. Please install it from https://github.com/astral-sh/uv"
    exit 1
fi

echo "Creating virtual environment in ${VENV_DIR} using uv..."
uv venv "${VENV_DIR}"

echo "Installing package locally (pip install -e .)..."
# We use the python from the newly created venv to ensure correct installation path
uv pip install --python "${VENV_DIR}/bin/python" -e .

echo "Autogenerating requirements.txt..."
uv pip freeze --python "${VENV_DIR}/bin/python" > requirements.txt

echo "Installing Chromium using playwright..."
# As requested: uv run playwright install chromium
uv run playwright install chromium

ln -s "${SCRIPT_DIR}/scripts/downlink" "${BINDIR}"
echo "Run the CLI with the 'downlink' command, e.g."
echo "  ${BINDIR}/downlink https://example.com/page"
