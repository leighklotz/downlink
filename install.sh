#!/usr/bin/env bash
set -euo pipefail

VENV_DIR=".venv"

echo "Creating virtual environment in ${VENV_DIR}..."
python3 -m venv "${VENV_DIR}"

echo "Activating venv..."
# shellcheck source=/dev/null
source "${VENV_DIR}/bin/activate"

echo "Upgrading pip, setuptools, wheel..."
python -m pip install --upgrade pip setuptools wheel

echo "Installing package locally (pip install .)..."
pip install .

echo "Installing Playwright browsers..."
# Try recommended install with deps; fall back to default if unavailable
if python -m playwright install --with-deps 2>/dev/null; then
  echo "Playwright browsers installed (with deps)."
else
  echo "Falling back to standard playwright install..."
  python -m playwright install
fi

echo "Done. To activate the virtual environment, run:"
echo "  source ${VENV_DIR}/bin/activate"
echo "Then run the CLI with the 'downlink' command, e.g."
echo "  downlink https://example.com/page"

echo "If you want to install in editable/develop mode instead, run inside the venv:"
echo "  pip install -e ."
