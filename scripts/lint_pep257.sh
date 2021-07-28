#!/usr/bin/env bash

# we use our own modified version of pep257.py stored in this directory
python ./scripts/pep257.py --add-ignore=D101,D104,D202,D210,D200,D205,D100,D400,D401,D204,D105 --count --match-dir='^((?!migrations).)*$'
