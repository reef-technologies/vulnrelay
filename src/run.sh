#!/usr/env/bin sh
# This script will be run by crontab
# so we need to change the working directory

set -euo pipefail

WORKDIR=/app

cd $WORKDIR || exit 1
uv run python main.py
