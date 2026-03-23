#!/usr/bin/env bash

set -e

if [ ! -d ".venv" ]; then
  echo "Error: .venv was not found. Run ./setup_and_run.sh first."
  exit 1
fi

source .venv/Scripts/activate
python main.py
