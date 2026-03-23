"""Execution helpers for query-driven Gmail automation rules."""

from __future__ import annotations

from gmail_base.planners.plan_loader import load_rules_plan
from gmail_base.services.message_service import (
    add_labels_to_messages,
    archive_messages,
    get_label_name_to_id_map,
    search_message_ids,
)


def preview_rules(plan_path: str) -> list[dict]:
    """Return preview details for each rule in the provided plan."""
    rules = load_rules_plan(plan_path)
    results: list[dict] = []

    for rule in rules:
        name = rule["name"]
        query = rule["query"]
        actions = rule["actions"]
        message_ids = search_message_ids(query)
        results.append(
            {
                "name": name,
                "query": query,
                "add_labels": actions["add_labels"],
                "archive": actions["archive"],
                "match_count": len(message_ids),
            }
        )

    return results


def apply_rules(plan_path: str, verbose: bool = False) -> list[dict]:
    """Apply query-driven rules and return structured execution results."""
    rules = load_rules_plan(plan_path)
    label_name_to_id = get_label_name_to_id_map()
    results: list[dict] = []

    for rule in rules:
        name = rule["name"]
        query = rule["query"]
        actions = rule["actions"]
        add_labels = actions["add_labels"]
        archive = actions["archive"]
        missing_labels = [label_name for label_name in add_labels if label_name not in label_name_to_id]

        if missing_labels:
            missing_labels_text = ", ".join(missing_labels)
            raise ValueError(f"Rule '{name}' references missing Gmail labels: {missing_labels_text}")

        message_ids = search_message_ids(query)
        label_ids = [label_name_to_id[label_name] for label_name in add_labels]
        updated_count = 0
        archived_count = 0

        if label_ids:
            updated_count = add_labels_to_messages(
                message_ids,
                label_ids,
                verbose=verbose,
            )

        if archive:
            archived_count = archive_messages(
                message_ids,
                verbose=verbose,
            )

        results.append(
            {
                "name": name,
                "query": query,
                "add_labels": add_labels,
                "archive": archive,
                "match_count": len(message_ids),
                "updated_count": updated_count,
                "archived_count": archived_count,
            }
        )

    return results
