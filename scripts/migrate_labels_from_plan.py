"""Preview or apply Gmail label migrations from a machine-readable plan."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from gmail_base.cli import parse_plan_execution_args
from gmail_base.planners.migration_plan_executor import (
    apply_label_migrations,
    preview_label_migrations,
)

DEFAULT_PLAN_PATH = "plans/gmail_organization/migrations.json"


def main() -> None:
    """Run label migration preview by default or apply changes with --apply."""
    execution_args = parse_plan_execution_args(sys.argv[1:], DEFAULT_PLAN_PATH)
    plan_path = execution_args.plan_path
    apply_mode = execution_args.apply_mode
    verbose = execution_args.verbose

    if apply_mode:
        print("Mode: APPLY")
        print()
        results = apply_label_migrations(plan_path, verbose=verbose)
        total_matched_messages = sum(result["match_count"] for result in results)
        total_submitted_messages = sum(result["updated_count"] for result in results)
        for result in results:
            new_labels = ", ".join(result["new_labels"])
            print(f"Old label: {result['old_label']}")
            print(f"New labels: {new_labels}")
            print(f"Matching messages: {result['match_count']}")
            print(f"Submitted messages: {result['updated_count']}")
        print()

        print(f"Total migrations: {len(results)}")
        print(f"Total matched messages: {total_matched_messages}")
        print(f"Total submitted messages: {total_submitted_messages}")
        return

    results = preview_label_migrations(plan_path)
    total_matched_messages = sum(result["match_count"] for result in results)

    print("Mode: PREVIEW")
    print()
    for result in results:
        new_labels = ", ".join(result["new_labels"])
        print(f"Old label: {result['old_label']}")
        print(f"New labels: {new_labels}")
        print(f"Matching messages: {result['match_count']}")
        print()

    print(f"Total migrations: {len(results)}")
    print(f"Total matched messages: {total_matched_messages}")
    print("Total submitted messages: 0")


if __name__ == "__main__":
    main()
