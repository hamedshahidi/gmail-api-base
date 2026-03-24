"""Preview or apply Gmail label cleanup from a machine-readable plan file."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from gmail_base.planners.cleanup_plan_executor import apply_cleanup, preview_cleanup

DEFAULT_PLAN_PATH = "plans/gmail_organization/cleanup.json"


def main() -> None:
    """Run cleanup preview by default or apply label removals when requested."""
    args = sys.argv[1:]

    plan_path = DEFAULT_PLAN_PATH
    apply_mode = False
    verbose = False

    for arg in args:
        if arg == "--apply":
            apply_mode = True
        elif arg == "--verbose":
            verbose = True
        else:
            plan_path = arg

    if apply_mode:
        print("Mode: APPLY")
        print()
        results = apply_cleanup(plan_path, verbose=verbose)
        total_matched_messages = sum(result["matched_messages"] for result in results)
        total_eligible_messages = sum(result["eligible_messages"] for result in results)
        total_updated_messages = sum(result["updated_messages"] for result in results)
        for result in results:
            require_labels = ", ".join(result["require_labels"]) if result["require_labels"] else "(none)"
            print(f"Cleanup rule: {result['name']}")
            print(f"Query: {result['query']}")
            print(f"Remove labels: {', '.join(result['remove_labels'])}")
            print(f"Require labels: {require_labels}")
            print(f"Skip if missing labels: {result['skip_if_missing_labels']}")
            print(f"Matching messages: {result['matched_messages']}")
            print(f"Eligible messages: {result['eligible_messages']}")
            print(f"Submitted messages: {result['updated_messages']}")
            print()

        print(f"Total cleanup rules: {len(results)}")
        print(f"Total matched messages: {total_matched_messages}")
        print(f"Total eligible messages: {total_eligible_messages}")
        print(f"Total submitted messages: {total_updated_messages}")
        return

    results = preview_cleanup(plan_path)
    total_matched_messages = sum(result["matched_messages"] for result in results)
    total_eligible_messages = sum(result["eligible_messages"] for result in results)

    print("Mode: PREVIEW")
    print()
    for result in results:
        require_labels = ", ".join(result["require_labels"]) if result["require_labels"] else "(none)"
        print(f"Cleanup rule: {result['name']}")
        print(f"Query: {result['query']}")
        print(f"Remove labels: {', '.join(result['remove_labels'])}")
        print(f"Require labels: {require_labels}")
        print(f"Skip if missing labels: {result['skip_if_missing_labels']}")
        print(f"Matching messages: {result['matched_messages']}")
        print(f"Eligible messages: {result['eligible_messages']}")
        print()

    print(f"Total cleanup rules: {len(results)}")
    print(f"Total matched messages: {total_matched_messages}")
    print(f"Total eligible messages: {total_eligible_messages}")
    print("Total updated messages: 0")


if __name__ == "__main__":
    main()
