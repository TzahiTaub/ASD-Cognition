#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="${VENV_DIR:-$PROJECT_ROOT/.venv}"
REQUIREMENTS="$PROJECT_ROOT/requirements.txt"

python3 -m venv "$VENV_DIR" --prompt "[asd]"
"$VENV_DIR/bin/python" -m pip install -r "$REQUIREMENTS"

SITE_PACKAGES="$("$VENV_DIR/bin/python" -c 'import sysconfig; print(sysconfig.get_paths()["purelib"])')"
printf '%s\n' "$PROJECT_ROOT/src" > "$SITE_PACKAGES/asd_cognition_project.pth"
