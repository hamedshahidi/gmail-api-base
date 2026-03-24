"""Execution helpers for plan-driven Gmail label cleanup."""

from __future__ import annotations

from gmail_base.planners.plan_loader import load_cleanup_plan
from gmail_base.services.message_service import (
    batch_modify_message_labels,
    get_label_name_to_id_map,
    get_messages_metadata,
    search_message_ids,
)


def preview_cleanup(plan_path: str) -> list[dict]:
    """Return preview details for each cleanup rule in the provided plan."""
    cleanup_rules = load_cleanup_plan(plan_path)
    label_name_to_id = get_label_name_to_id_map()
    results: list[dict] = []

    for cleanup_rule in cleanup_rules:
        result = _build_cleanup_result(cleanup_rule, label_name_to_id)
        result.pop("eligible_message_ids")
        result.pop("remove_label_ids")
        results.append(result)

    return results


def apply_cleanup(plan_path: str, verbose: bool = False) -> list[dict]:
    """Apply label cleanup rules and return structured execution results."""
    cleanup_rules = load_cleanup_plan(plan_path)
    label_name_to_id = get_label_name_to_id_map()
    results: list[dict] = []

    for cleanup_rule in cleanup_rules:
        result = _build_cleanup_result(cleanup_rule, label_name_to_id)
        eligible_message_ids = result.pop("eligible_message_ids")
        remove_label_ids = result.pop("remove_label_ids")
        updated_messages = batch_modify_message_labels(
            eligible_message_ids,
            remove_label_ids=remove_label_ids,
            verbose=verbose,
        )
        result["updated_messages"] = updated_messages
        results.append(result)

    return results


def _build_cleanup_result(cleanup_rule: dict, label_name_to_id: dict[str, str]) -> dict:
    """Build the structured cleanup result for a single cleanup rule."""
    name = cleanup_rule["name"]
    query = cleanup_rule["query"]
    remove_labels = cleanup_rule["remove_labels"]
    require_labels = cleanup_rule["require_labels"]
    skip_if_missing_labels = cleanup_rule["skip_if_missing_labels"]

    _validate_referenced_labels(name, remove_labels, require_labels, label_name_to_id)

    matched_message_ids = search_message_ids(query)
    eligible_message_ids = _get_eligible_message_ids(
        matched_message_ids,
        remove_labels,
        require_labels,
        skip_if_missing_labels,
        label_name_to_id,
    )

    return {
        "name": name,
        "query": query,
        "remove_labels": remove_labels,
        "require_labels": require_labels,
        "skip_if_missing_labels": skip_if_missing_labels,
        "matched_messages": len(matched_message_ids),
        "eligible_messages": len(eligible_message_ids),
        "eligible_message_ids": eligible_message_ids,
        "remove_label_ids": [label_name_to_id[label_name] for label_name in remove_labels],
    }


def _validate_referenced_labels(
    rule_name: str,
    remove_labels: list[str],
    require_labels: list[str],
    label_name_to_id: dict[str, str],
) -> None:
    """Raise a clear error if a cleanup rule references any missing Gmail labels."""
    missing_remove_labels = [label_name for label_name in remove_labels if label_name not in label_name_to_id]
    if missing_remove_labels:
        missing_labels_text = ", ".join(missing_remove_labels)
        raise ValueError(
            f"Cleanup rule '{rule_name}' references missing Gmail labels in remove_labels: {missing_labels_text}"
        )

    missing_required_labels = [
        label_name for label_name in require_labels if label_name not in label_name_to_id
    ]
    if missing_required_labels:
        missing_labels_text = ", ".join(missing_required_labels)
        raise ValueError(
            f"Cleanup rule '{rule_name}' references missing Gmail labels in require_labels: {missing_labels_text}"
        )


def _get_eligible_message_ids(
    message_ids: list[str],
    remove_labels: list[str],
    require_labels: list[str],
    skip_if_missing_labels: bool,
    label_name_to_id: dict[str, str],
) -> list[str]:
    """Return matching message IDs that are eligible for label removal."""
    if not message_ids:
        return []

    remove_label_ids = {label_name_to_id[label_name] for label_name in remove_labels}
    required_label_ids = {label_name_to_id[label_name] for label_name in require_labels}
    messages_metadata = get_messages_metadata(message_ids)
    eligible_message_ids: list[str] = []

    for message_metadata in messages_metadata:
        message_id = message_metadata.get("id")
        current_label_ids = set(message_metadata.get("labelIds", []))

        if not message_id:
            continue

        if not current_label_ids.intersection(remove_label_ids):
            continue

        has_all_required_labels = required_label_ids.issubset(current_label_ids)
        if required_label_ids and skip_if_missing_labels and not has_all_required_labels:
            continue

        eligible_message_ids.append(message_id)

    return eligible_message_ids
