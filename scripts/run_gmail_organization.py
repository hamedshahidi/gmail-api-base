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
PIPELINE_COMMANDS = ("labels", "migrations", "rules", "cleanup")


def main() -> None:
    """Dispatch to one of the existing Gmail organization plan scripts."""
    args = sys.argv[1:]
    if not args:
        _raise_usage_error("Missing command.")

    command = args[0]
    forwarded_args = args[1:]

    if command == "pipeline":
        _validate_pipeline_args(forwarded_args)
        _run_pipeline(forwarded_args)
        return

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


def _validate_pipeline_args(args: list[str]) -> None:
    """Reject unsupported positional arguments for the pipeline command."""
    positional_args = [arg for arg in args if not arg.startswith("--")]
    if positional_args:
        args_text = ", ".join(positional_args)
        raise SystemExit(
            f"pipeline does not support positional arguments: {args_text}\n"
            f"{_usage_text()}"
        )

    unsupported_flags = [arg for arg in args if arg not in {"--apply", "--verbose"}]
    if unsupported_flags:
        flags_text = ", ".join(unsupported_flags)
        raise SystemExit(
            f"pipeline does not support these flags: {flags_text}\n"
            f"{_usage_text()}"
        )


def _run_pipeline(args: list[str]) -> None:
    """Run the full labels-to-cleanup pipeline using default plan paths."""
    apply_mode = "--apply" in args
    modifying_args = [arg for arg in args if arg in {"--apply", "--verbose"}]
    labels_executed = False

    print("Pipeline: labels -> migrations -> rules -> cleanup")
    print()

    for command in PIPELINE_COMMANDS:
        if command == "labels" and not apply_mode:
            print("=== LABELS ===")
            print("Skipping labels in preview pipeline mode. Use --apply to include label creation.")
            print()
            continue

        forwarded_args = [] if command == "labels" else modifying_args
        if command == "labels":
            labels_executed = True
        _run_pipeline_step(command, forwarded_args)

    _print_pipeline_summary(labels_executed, apply_mode)


def _run_pipeline_step(command: str, forwarded_args: list[str]) -> None:
    """Execute a single named pipeline step."""
    print(f"=== {command.upper()} ===")
    _run_script(SCRIPT_PATHS[command], forwarded_args)
    print()


def _print_pipeline_summary(labels_executed: bool, apply_mode: bool) -> None:
    """Print a short summary after the pipeline completes."""
    labels_status = "executed" if labels_executed else "skipped"
    pipeline_mode = "APPLY" if apply_mode else "PREVIEW"

    print("Pipeline complete.")
    print(f"Pipeline mode: {pipeline_mode}")
    print(f"Labels step: {labels_status}")


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
        "<labels|migrations|rules|cleanup|pipeline> [plan_path] [--apply] [--verbose]\n"
        "Note: labels accepts only an optional plan path. "
        "pipeline accepts only --apply and --verbose, uses default plan paths, "
        "and skips labels unless --apply is provided."
    )


if __name__ == "__main__":
    main()
