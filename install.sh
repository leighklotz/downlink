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

echo "Creating virtual environment in ${VENV_DIR}..."
python3 -m venv "${VENV_DIR}"

echo "Activating venv..."
# shellcheck source=/dev/null
source "${VENV_DIR}/bin/activate"

echo "Upgrading pip, setuptools, wheel..."
python -m pip install --upgrade pip setuptools wheel

echo "Installing package locally (pip install -e .)..."
pip install -e .

echo "Installing Playwright browsers..."
# Try recommended install with deps; fall back to default if unavailable
if python -m playwright install --with-deps 2>/dev/null; then
  echo "Playwright browsers installed (with deps)."
else
  echo "Falling back to standard playwright install..."
  python -m playwright install
fi

ln -s "${SCRIPT_DIR}/scripts/downlink" "${BINDIR}"
echo "Run the CLI with the 'downlink' command, e.g."
echo "  ${BINDIR}/downlink https://example.com/page"
