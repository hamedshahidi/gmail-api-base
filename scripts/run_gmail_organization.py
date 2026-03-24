"""Unified entry point for running Gmail organization plan scripts."""

from __future__ import annotations

import runpy
import sys
from pathlib import Path

DEFAULT_PLAN_DIRECTORY = Path("plans/gmail_organization")
SCRIPT_PATHS = {
    "labels": Path(__file__).resolve().parent / "create_labels_from_plan.py",
    "migrations": Path(__file__).resolve().parent / "migrate_labels_from_plan.py",
    "rules": Path(__file__).resolve().parent / "apply_rules_from_plan.py",
    "cleanup": Path(__file__).resolve().parent / "cleanup_labels_from_plan.py",
}
PIPELINE_COMMANDS = ("labels", "migrations", "rules", "cleanup")
PIPELINE_PLAN_FILES = {
    "labels": "labels.json",
    "migrations": "migrations.json",
    "rules": "rules.json",
    "cleanup": "cleanup.json",
}


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
    positional_args = _pipeline_positional_args(args)
    if positional_args:
        args_text = ", ".join(positional_args)
        raise SystemExit(
            f"pipeline does not support positional arguments: {args_text}\n"
            f"{_usage_text()}"
        )

    unsupported_flags = _pipeline_unsupported_flags(args)
    if unsupported_flags:
        flags_text = ", ".join(unsupported_flags)
        raise SystemExit(
            f"pipeline does not support these flags: {flags_text}\n"
            f"{_usage_text()}"
        )


def _run_pipeline(args: list[str]) -> None:
    """Run the full labels-to-cleanup pipeline using default plan paths."""
    plan_directory = _get_pipeline_plan_directory(args)
    apply_mode = "--apply" in args
    modifying_args = [arg for arg in args if arg in {"--apply", "--verbose"}]
    labels_executed = False

    print("Pipeline: labels -> migrations -> rules -> cleanup")
    print(f"Plan directory: {plan_directory}")
    print()

    for command in PIPELINE_COMMANDS:
        if command == "labels" and not apply_mode:
            print("=== LABELS ===")
            print("Skipping labels in preview pipeline mode. Use --apply to include label creation.")
            print()
            continue

        plan_path = plan_directory / PIPELINE_PLAN_FILES[command]
        forwarded_args = [str(plan_path)] if command == "labels" else [str(plan_path), *modifying_args]
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


def _get_pipeline_plan_directory(args: list[str]) -> Path:
    """Return the requested pipeline plan directory or the default directory."""
    for index, arg in enumerate(args):
        if arg == "--plan-dir":
            return Path(args[index + 1])

    return DEFAULT_PLAN_DIRECTORY


def _pipeline_positional_args(args: list[str]) -> list[str]:
    """Return positional pipeline arguments after accounting for flag values."""
    positional_args: list[str] = []
    skip_next = False

    for arg in args:
        if skip_next:
            skip_next = False
            continue

        if arg == "--plan-dir":
            skip_next = True
            continue

        if not arg.startswith("--"):
            positional_args.append(arg)

    return positional_args


def _pipeline_unsupported_flags(args: list[str]) -> list[str]:
    """Return unsupported pipeline flags, including missing --plan-dir values."""
    unsupported_flags: list[str] = []
    index = 0

    while index < len(args):
        arg = args[index]
        if arg in {"--apply", "--verbose"}:
            index += 1
            continue

        if arg == "--plan-dir":
            if index + 1 >= len(args) or args[index + 1].startswith("--"):
                unsupported_flags.append("--plan-dir")
                index += 1
                continue

            index += 2
            continue

        if arg.startswith("--"):
            unsupported_flags.append(arg)

        index += 1

    return unsupported_flags


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
        "<labels|migrations|rules|cleanup|pipeline> [plan_path] [--apply] [--verbose] [--plan-dir PATH]\n"
        "Note: labels accepts only an optional plan path. "
        "pipeline accepts only --apply, --verbose, and --plan-dir, uses default plan paths unless overridden, "
        "and skips labels unless --apply is provided."
    )


if __name__ == "__main__":
    main()
