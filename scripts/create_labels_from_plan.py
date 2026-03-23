"""Create Gmail labels from a machine-readable plan file."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from gmail_base.planners.label_plan_executor import create_labels_from_plan

DEFAULT_PLAN_PATH = "plans/gmail_organization/labels.json"


def main() -> None:
    """Create missing Gmail labels from the requested plan."""
    plan_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PLAN_PATH
    results = create_labels_from_plan(plan_path)
    created_labels = sorted(name for name, status in results.items() if status == "created")
    existing_labels = sorted(name for name, status in results.items() if status == "exists")

    print("Created labels:")
    for label_name in created_labels:
        print(label_name)

    print()
    print("Existing labels:")
    for label_name in existing_labels:
        print(label_name)

    print()
    print(f"Created: {len(created_labels)}")
    print(f"Already existed: {len(existing_labels)}")
    print(f"Total planned: {len(results)}")


if __name__ == "__main__":
    main()
