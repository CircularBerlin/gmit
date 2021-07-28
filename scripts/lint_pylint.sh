#!/usr/bin/env bash

# just to be really hard on yourself
pylint `find src -name "*.py"` --max-line-length=140 \
    -d E1101 \
    -d C0103 \
    -d C0116 \
    -d W0511 \
    -d C0115 \
    -d C0114 \
    -d R0903 \
    -d W0621 \
    -d C0301 \
    -d R0801 \
    -d W0212 \
    -d W0235 \
    -d W0223 \
    -d R0201 \
    -d R1705 \
    -d R0914 \
    -d C0302
