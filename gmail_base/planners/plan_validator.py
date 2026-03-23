"""Validation helpers for machine-readable plan data."""

from __future__ import annotations


def validate_label_plan_data(data: dict) -> list[str]:
    """Validate label plan data and return a cleaned label list."""
    if "labels" not in data:
        raise ValueError("Label plan must contain a top-level 'labels' key.")

    labels = data["labels"]
    if not isinstance(labels, list):
        raise ValueError("Label plan 'labels' must be a list.")

    cleaned_labels: list[str] = []
    seen_labels: set[str] = set()

    for index, label in enumerate(labels):
        if not isinstance(label, str):
            raise ValueError(f"Label at index {index} must be a string.")

        cleaned_label = label.strip()
        if not cleaned_label:
            raise ValueError(f"Label at index {index} must be a non-empty string.")

        if cleaned_label in seen_labels:
            raise ValueError(f"Duplicate label found in plan: {cleaned_label}")

        seen_labels.add(cleaned_label)
        cleaned_labels.append(cleaned_label)

    return cleaned_labels

