"""Preview or apply query-driven Gmail automation rules from a plan file."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from gmail_base.planners.rules_plan_executor import apply_rules, preview_rules

DEFAULT_PLAN_PATH = "plans/gmail_organization/rules.json"


def main() -> None:
    """Run rules preview by default or apply rules when explicitly requested."""
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
        results = apply_rules(plan_path, verbose=verbose)
        total_matched_messages = sum(result["match_count"] for result in results)
        total_eligible_messages = sum(result["eligible_count"] for result in results)
        total_updated_messages = sum(result["updated_count"] for result in results)
        total_archived_messages = sum(result["archived_count"] for result in results)
        for result in results:
            add_labels = ", ".join(result["add_labels"]) if result["add_labels"] else "(none)"
            exclude_labels = ", ".join(result["exclude_labels"]) if result["exclude_labels"] else "(none)"
            print(f"Rule: {result['name']}")
            print(f"Query: {result['query']}")
            print(f"Add labels: {add_labels}")
            print(f"Exclude labels: {exclude_labels}")
            print(f"Archive: {result['archive']}")
            print(f"Matching messages: {result['match_count']}")
            print(f"Eligible messages: {result['eligible_count']}")
            print(f"Submitted messages: {result['updated_count']}")
            print(f"Archived messages: {result['archived_count']}")
            print()

        print(f"Total rules: {len(results)}")
        print(f"Total matched messages: {total_matched_messages}")
        print(f"Total eligible messages: {total_eligible_messages}")
        print(f"Total submitted messages: {total_updated_messages}")
        print(f"Total archived messages: {total_archived_messages}")
        return

    results = preview_rules(plan_path)
    total_matched_messages = sum(result["match_count"] for result in results)
    total_eligible_messages = sum(result["eligible_count"] for result in results)

    print("Mode: PREVIEW")
    print()
    for result in results:
        add_labels = ", ".join(result["add_labels"]) if result["add_labels"] else "(none)"
        exclude_labels = ", ".join(result["exclude_labels"]) if result["exclude_labels"] else "(none)"
        print(f"Rule: {result['name']}")
        print(f"Query: {result['query']}")
        print(f"Add labels: {add_labels}")
        print(f"Exclude labels: {exclude_labels}")
        print(f"Archive: {result['archive']}")
        print(f"Matching messages: {result['match_count']}")
        print(f"Eligible messages: {result['eligible_count']}")
        print()

    print(f"Total rules: {len(results)}")
    print(f"Total matched messages: {total_matched_messages}")
    print(f"Total eligible messages: {total_eligible_messages}")
    print("Total submitted messages: 0")
    print("Total archived messages: 0")


if __name__ == "__main__":
    main()
