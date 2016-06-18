#!/usr/bin/env bash
SCRIPT_DIR=`dirname "$0"`
SCRIPT_FILE="$SCRIPT_DIR/theme_gen.py"
python3 ${SCRIPT_FILE} "$@"
