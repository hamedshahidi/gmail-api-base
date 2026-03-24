"""File loaders for machine-readable automation plans."""

from __future__ import annotations

import json
from pathlib import Path

from gmail_base.planners.plan_validator import (
    validate_cleanup_plan_data,
    validate_label_plan_data,
    validate_migration_plan_data,
    validate_rules_plan_data,
)


def load_plan_file(path: str) -> dict:
    """Load a JSON or YAML plan file and return its top-level object."""
    file_path = Path(path)

    try:
        contents = file_path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise ValueError(f"Plan file not found: {path}") from exc

    suffix = file_path.suffix.lower()
    if suffix == ".json":
        data = _load_json_contents(contents, path)
    elif suffix in {".yaml", ".yml"}:
        data = _load_yaml_contents(contents, path)
    else:
        raise ValueError(
            f"Unsupported plan file type for '{path}'. "
            "Use .json, .yaml, or .yml."
        )

    if not isinstance(data, dict):
        raise ValueError(
            f"Plan file '{path}' must contain a top-level object."
        )

    return data


def load_json_file(path: str) -> dict:
    """Load a JSON plan file and return its top-level object."""
    file_path = Path(path)
    if file_path.suffix.lower() != ".json":
        raise ValueError(f"Expected a .json plan file, got: {path}")

    return load_plan_file(path)


def _load_json_contents(contents: str, path: str) -> dict:
    """Load JSON contents from a plan file."""
    try:
        return json.loads(contents)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in plan file '{path}': {exc.msg}") from exc


def _load_yaml_contents(contents: str, path: str) -> dict:
    """Load YAML contents from a plan file when PyYAML is available."""
    try:
        import yaml
    except ImportError as exc:
        raise ValueError(
            f"YAML plan support for '{path}' requires PyYAML to be installed."
        ) from exc

    try:
        return yaml.safe_load(contents)
    except yaml.YAMLError as exc:
        raise ValueError(f"Invalid YAML in plan file '{path}': {exc}") from exc


def load_label_plan(path: str) -> list[str]:
    """Load and validate label names from a label plan file."""
    data = load_plan_file(path)
    return validate_label_plan_data(data)


def load_migration_plan(path: str) -> list[dict]:
    """Load and validate migration entries from a migration plan file."""
    data = load_plan_file(path)
    return validate_migration_plan_data(data)


def load_rules_plan(path: str) -> list[dict]:
    """Load and validate rule entries from a rules plan file."""
    data = load_plan_file(path)
    return validate_rules_plan_data(data)


def load_cleanup_plan(path: str) -> list[dict]:
    """Load and validate cleanup rule entries from a cleanup plan file."""
    data = load_plan_file(path)
    return validate_cleanup_plan_data(data)
