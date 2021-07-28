#!/usr/bin/env bash

# lint it using pyflakes
python3 -m pyflakes `find src -name "*.py"`
