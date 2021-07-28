#!/usr/bin/env bash

set -e
set -v

./scripts/lint_style.sh
./scripts/lint_pyflakes.sh
./scripts/lint_pylint.sh
./scripts/lint_mypy.sh
./scripts/lint_pep257.sh
