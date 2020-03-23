#!/bin/bash
set -euxo pipefail
export TOXENV="ansible-lint"

python -m tox

# Delete the .tox/ directory with the venv libs
rm -rf .tox/
