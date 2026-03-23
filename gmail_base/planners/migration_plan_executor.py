"""Execution helpers for label migration plans."""

from __future__ import annotations

from gmail_base.planners.plan_loader import load_migration_plan
from gmail_base.services.message_service import (
    add_labels_to_messages,
    get_label_name_to_id_map,
    search_message_ids,
)


def preview_label_migrations(plan_path: str) -> list[dict]:
    """Return preview details for each label migration in the plan."""
    migrations = load_migration_plan(plan_path)
    results: list[dict] = []

    for migration in migrations:
        old_label = migration["old_label"]
        new_labels = migration["new_labels"]
        message_ids = search_message_ids(f'label:"{old_label}"')
        results.append(
            {
                "old_label": old_label,
                "new_labels": new_labels,
                "match_count": len(message_ids),
            }
        )

    return results


def apply_label_migrations(plan_path: str, verbose: bool = False) -> list[dict]:
    """Apply label migrations by adding new labels to matching messages."""
    migrations = load_migration_plan(plan_path)
    label_name_to_id = get_label_name_to_id_map()
    results: list[dict] = []

    for migration in migrations:
        old_label = migration["old_label"]
        new_labels = migration["new_labels"]
        missing_labels = [label_name for label_name in new_labels if label_name not in label_name_to_id]

        if missing_labels:
            missing_labels_text = ", ".join(missing_labels)
            raise ValueError(
                f"Migration references missing Gmail labels for '{old_label}': {missing_labels_text}"
            )

        message_ids = search_message_ids(f'label:"{old_label}"')
        label_ids = [label_name_to_id[label_name] for label_name in new_labels]
        target_labels = ", ".join(new_labels)
        print(f"Applying migration: {old_label}")
        print(f"Matching messages: {len(message_ids)}")
        print(f"Target labels: {target_labels}")
        updated_count = add_labels_to_messages(
            message_ids,
            label_ids,
            verbose=verbose,
        )
        print(f"Updated messages: {updated_count}")
        print()
        results.append(
            {
                "old_label": old_label,
                "new_labels": new_labels,
                "match_count": len(message_ids),
                "updated_count": updated_count,
            }
        )

    return results
