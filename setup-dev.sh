#!/usr/bin/env bash

set -euo pipefail

if ! command -v uv &> /dev/null; then
  echo "uv cannot not be found, please install it and try again"
fi

uv sync
if [ -z "${CI:-}" ]; then
  uv run pre-commit install --install-hooks
fi

ENV_DIR=./envs/dev

if [ ! -f "$ENV_DIR/.env" ]; then
    echo "Creating .env file"
    cp "$ENV_DIR/.env.template" "$ENV_DIR/.env"
fi

ln -sf "${ENV_DIR}/.env" .env
