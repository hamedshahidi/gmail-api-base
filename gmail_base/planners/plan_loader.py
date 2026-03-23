"""File loaders for machine-readable automation plans."""

from __future__ import annotations

import json
from pathlib import Path

from gmail_base.planners.plan_validator import (
    validate_label_plan_data,
    validate_migration_plan_data,
    validate_rules_plan_data,
)


def load_json_file(path: str) -> dict:
    """Load a JSON file and return its top-level object."""
    file_path = Path(path)

    try:
        contents = file_path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise ValueError(f"Plan file not found: {path}") from exc

    try:
        data = json.loads(contents)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in plan file '{path}': {exc.msg}") from exc

    if not isinstance(data, dict):
        raise ValueError(f"Plan file '{path}' must contain a top-level JSON object.")

    return data


def load_label_plan(path: str) -> list[str]:
    """Load and validate label names from a label plan file."""
    data = load_json_file(path)
    return validate_label_plan_data(data)


def load_migration_plan(path: str) -> list[dict]:
    """Load and validate migration entries from a migration plan file."""
    data = load_json_file(path)
    return validate_migration_plan_data(data)


def load_rules_plan(path: str) -> list[dict]:
    """Load and validate rule entries from a rules plan file."""
    data = load_json_file(path)
    return validate_rules_plan_data(data)
