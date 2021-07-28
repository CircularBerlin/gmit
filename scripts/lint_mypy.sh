#!/usr/bin/env bash

# find src -name "*.py"

python3 -m mypy \
    --warn-unused-ignores \
    --show-error-codes \
    --ignore-missing-imports \
    --disallow-untyped-defs `find src -name "*.py"`
