#!/usr/bin/env bash
set -euo pipefail

VENV_DIR=".venv"

echo "Creating virtual environment in ${VENV_DIR}..."
python3 -m venv "${VENV_DIR}"

echo "Activating venv and upgrading pip..."
# shellcheck source=/dev/null
source "${VENV_DIR}/bin/activate"
python -m pip install --upgrade pip setuptools wheel

echo "Installing package locally (pip install .)..."
pip install .

echo "Done. To activate the virtual environment, run:"
echo "  source ${VENV_DIR}/bin/activate"
echo "Then run the CLI with the `downlink` command."