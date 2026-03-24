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
        exclude_labels = rule["exclude_labels"]
        actions = rule["actions"]
        add_labels = actions["add_labels"]
        archive = actions["archive"]
        matched_message_ids, eligible_message_ids = _get_matched_and_eligible_message_ids(
            query,
            exclude_labels,
        )
        skipped_count = len(matched_message_ids) - len(eligible_message_ids)
        results.append(
            {
                "name": name,
                "query": query,
                "add_labels": add_labels,
                "exclude_labels": exclude_labels,
                "archive": archive,
                "match_count": len(matched_message_ids),
                "eligible_count": len(eligible_message_ids),
                "skipped_count": skipped_count,
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
        exclude_labels = rule["exclude_labels"]
        actions = rule["actions"]
        add_labels = actions["add_labels"]
        archive = actions["archive"]
        _validate_rule_labels(name, add_labels, exclude_labels, label_name_to_id)

        matched_message_ids, eligible_message_ids = _get_matched_and_eligible_message_ids(
            query,
            exclude_labels,
        )
        skipped_count = len(matched_message_ids) - len(eligible_message_ids)
        label_ids = [label_name_to_id[label_name] for label_name in add_labels]
        updated_count = 0
        archived_count = 0

        if label_ids:
            updated_count = add_labels_to_messages(
                eligible_message_ids,
                label_ids,
                verbose=verbose,
            )

        if archive:
            archived_count = archive_messages(
                eligible_message_ids,
                verbose=verbose,
            )

        results.append(
            {
                "name": name,
                "query": query,
                "add_labels": add_labels,
                "exclude_labels": exclude_labels,
                "archive": archive,
                "match_count": len(matched_message_ids),
                "eligible_count": len(eligible_message_ids),
                "skipped_count": skipped_count,
                "updated_count": updated_count,
                "archived_count": archived_count,
            }
        )

    return results


def _get_matched_and_eligible_message_ids(
    query: str,
    exclude_labels: list[str],
) -> tuple[list[str], list[str]]:
    """Return matched and eligible message IDs for a rule query."""
    matched_message_ids = search_message_ids(query)

    if not exclude_labels:
        return matched_message_ids, matched_message_ids

    eligible_message_ids = search_message_ids(_build_eligible_query(query, exclude_labels))
    return matched_message_ids, eligible_message_ids


def _build_eligible_query(query: str, exclude_labels: list[str]) -> str:
    """Return the Gmail query used to exclude already-handled messages."""
    if not exclude_labels:
        return query

    exclusion_query = " ".join(f'-label:"{label_name}"' for label_name in exclude_labels)
    return f"{query} {exclusion_query}"


def _validate_rule_labels(
    rule_name: str,
    add_labels: list[str],
    exclude_labels: list[str],
    label_name_to_id: dict[str, str],
) -> None:
    """Raise a clear error if a rule references missing Gmail labels."""
    missing_add_labels = [label_name for label_name in add_labels if label_name not in label_name_to_id]
    if missing_add_labels:
        missing_labels_text = ", ".join(missing_add_labels)
        raise ValueError(f"Rule '{rule_name}' references missing Gmail add_labels: {missing_labels_text}")

    missing_exclude_labels = [
        label_name for label_name in exclude_labels if label_name not in label_name_to_id
    ]
    if missing_exclude_labels:
        missing_labels_text = ", ".join(missing_exclude_labels)
        raise ValueError(
            f"Rule '{rule_name}' references missing Gmail exclude_labels: {missing_labels_text}"
        )
