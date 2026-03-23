#!/usr/bin/env bash

set -e

if [ ! -d ".venv" ]; then
  python -m venv .venv
fi

source .venv/Scripts/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python main.py
