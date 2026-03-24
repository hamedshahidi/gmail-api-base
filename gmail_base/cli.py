"""Reusable CLI helpers for thin plan-driven scripts."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PlanExecutionArgs:
    """Normalized CLI arguments for preview/apply plan execution scripts."""

    plan_path: str
    apply_mode: bool
    verbose: bool


def parse_optional_plan_path(args: list[str], default_plan_path: str) -> str:
    """Return the first positional plan path argument or the default plan path."""
    return args[0] if args else default_plan_path


def parse_plan_execution_args(args: list[str], default_plan_path: str) -> PlanExecutionArgs:
    """Parse common plan-path, apply, and verbose flags for thin scripts."""
    plan_path = default_plan_path
    apply_mode = False
    verbose = False

    for arg in args:
        if arg == "--apply":
            apply_mode = True
        elif arg == "--verbose":
            verbose = True
        else:
            plan_path = arg

    return PlanExecutionArgs(
        plan_path=plan_path,
        apply_mode=apply_mode,
        verbose=verbose,
    )
