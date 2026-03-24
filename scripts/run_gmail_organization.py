"""Unified entry point for running Gmail organization plan scripts."""

from __future__ import annotations

import runpy
import sys
from pathlib import Path

SCRIPT_PATHS = {
    "labels": Path(__file__).resolve().parent / "create_labels_from_plan.py",
    "migrations": Path(__file__).resolve().parent / "migrate_labels_from_plan.py",
    "rules": Path(__file__).resolve().parent / "apply_rules_from_plan.py",
    "cleanup": Path(__file__).resolve().parent / "cleanup_labels_from_plan.py",
}


def main() -> None:
    """Dispatch to one of the existing Gmail organization plan scripts."""
    args = sys.argv[1:]
    if not args:
        _raise_usage_error("Missing command.")

    command = args[0]
    forwarded_args = args[1:]

    if command not in SCRIPT_PATHS:
        _raise_usage_error(f"Unknown command: {command}")

    if command == "labels":
        _validate_labels_args(forwarded_args)

    _run_script(SCRIPT_PATHS[command], forwarded_args)


def _validate_labels_args(args: list[str]) -> None:
    """Reject unsupported flags for the labels command."""
    unsupported_flags = [arg for arg in args if arg.startswith("--")]
    if unsupported_flags:
        flags_text = ", ".join(unsupported_flags)
        raise SystemExit(
            f"labels does not support these flags: {flags_text}\n"
            f"{_usage_text()}"
        )

    if len(args) > 1:
        raise SystemExit(
            "labels accepts at most one optional plan path.\n"
            f"{_usage_text()}"
        )


def _run_script(script_path: Path, forwarded_args: list[str]) -> None:
    """Execute an existing script with forwarded command-line arguments."""
    original_argv = sys.argv[:]
    try:
        sys.argv = [str(script_path), *forwarded_args]
        runpy.run_path(str(script_path), run_name="__main__")
    finally:
        sys.argv = original_argv


def _raise_usage_error(message: str) -> None:
    """Exit with a short usage message for invalid unified CLI input."""
    raise SystemExit(f"{message}\n{_usage_text()}")


def _usage_text() -> str:
    """Return the unified CLI usage text."""
    return (
        "Usage: python scripts/run_gmail_organization.py "
        "<labels|migrations|rules|cleanup> [plan_path] [--apply] [--verbose]\n"
        "Note: --apply and --verbose apply only to migrations, rules, and cleanup."
    )


if __name__ == "__main__":
    main()
