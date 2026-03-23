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


def validate_migration_plan_data(data: dict) -> list[dict]:
    """Validate migration plan data and return cleaned migration entries."""
    if "migrations" not in data:
        raise ValueError("Migration plan must contain a top-level 'migrations' key.")

    migrations = data["migrations"]
    if not isinstance(migrations, list):
        raise ValueError("Migration plan 'migrations' must be a list.")

    cleaned_migrations: list[dict] = []
    seen_old_labels: set[str] = set()

    for index, migration in enumerate(migrations):
        if not isinstance(migration, dict):
            raise ValueError(f"Migration at index {index} must be an object.")

        if "old_label" not in migration:
            raise ValueError(f"Migration at index {index} must contain 'old_label'.")
        if "new_labels" not in migration:
            raise ValueError(f"Migration at index {index} must contain 'new_labels'.")

        old_label = migration["old_label"]
        new_labels = migration["new_labels"]

        if not isinstance(old_label, str):
            raise ValueError(f"Migration 'old_label' at index {index} must be a string.")
        cleaned_old_label = old_label.strip()
        if not cleaned_old_label:
            raise ValueError(f"Migration 'old_label' at index {index} must be non-empty.")
        if cleaned_old_label in seen_old_labels:
            raise ValueError(f"Duplicate migration old_label found: {cleaned_old_label}")

        if not isinstance(new_labels, list) or not new_labels:
            raise ValueError(
                f"Migration 'new_labels' for '{cleaned_old_label}' must be a non-empty list."
            )

        cleaned_new_labels: list[str] = []
        for new_label_index, new_label in enumerate(new_labels):
            if not isinstance(new_label, str):
                raise ValueError(
                    f"Migration new label at index {new_label_index} for '{cleaned_old_label}' must be a string."
                )

            cleaned_new_label = new_label.strip()
            if not cleaned_new_label:
                raise ValueError(
                    f"Migration new label at index {new_label_index} for '{cleaned_old_label}' must be non-empty."
                )

            cleaned_new_labels.append(cleaned_new_label)

        seen_old_labels.add(cleaned_old_label)
        cleaned_migrations.append(
            {
                "old_label": cleaned_old_label,
                "new_labels": cleaned_new_labels,
            }
        )

    return cleaned_migrations
