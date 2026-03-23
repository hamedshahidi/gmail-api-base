"""Preview or apply Gmail label migrations from a machine-readable plan."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from gmail_base.planners.migration_plan_executor import (
    apply_label_migrations,
    preview_label_migrations,
)

DEFAULT_PLAN_PATH = "plans/gmail_organization/migrations.json"


def main() -> None:
    """Run label migration preview by default or apply changes with --apply."""
    apply_mode = False
    plan_path = DEFAULT_PLAN_PATH

    for argument in sys.argv[1:]:
        if argument == "--apply":
            apply_mode = True
        else:
            plan_path = argument

    if apply_mode:
        results = apply_label_migrations(plan_path)
        total_matched_messages = sum(result["match_count"] for result in results)
        total_updated_messages = sum(result["updated_count"] for result in results)

        print("Apply mode")
        print()
        for result in results:
            new_labels = ", ".join(result["new_labels"])
            print(f"Old label: {result['old_label']}")
            print(f"New labels: {new_labels}")
            print(f"Matching messages: {result['match_count']}")
            print(f"Updated messages: {result['updated_count']}")
            print()

        print(f"Total migrations: {len(results)}")
        print(f"Total matched messages: {total_matched_messages}")
        print(f"Total updated messages: {total_updated_messages}")
        return

    results = preview_label_migrations(plan_path)
    total_matched_messages = sum(result["match_count"] for result in results)

    print("Preview mode")
    print()
    for result in results:
        new_labels = ", ".join(result["new_labels"])
        print(f"Old label: {result['old_label']}")
        print(f"New labels: {new_labels}")
        print(f"Matching messages: {result['match_count']}")
        print()

    print(f"Total migrations: {len(results)}")
    print(f"Total matched messages: {total_matched_messages}")


if __name__ == "__main__":
    main()
