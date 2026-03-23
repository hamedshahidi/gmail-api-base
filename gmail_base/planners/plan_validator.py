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


def validate_rules_plan_data(data: dict) -> list[dict]:
    """Validate rules plan data and return cleaned rule entries."""
    if "rules" not in data:
        raise ValueError("Rules plan must contain a top-level 'rules' key.")

    rules = data["rules"]
    if not isinstance(rules, list):
        raise ValueError("Rules plan 'rules' must be a list.")

    cleaned_rules: list[dict] = []
    seen_rule_names: set[str] = set()

    for index, rule in enumerate(rules):
        if not isinstance(rule, dict):
            raise ValueError(f"Rule at index {index} must be an object.")

        if "name" not in rule:
            raise ValueError(f"Rule at index {index} must contain 'name'.")
        if "query" not in rule:
            raise ValueError(f"Rule at index {index} must contain 'query'.")
        if "actions" not in rule:
            raise ValueError(f"Rule at index {index} must contain 'actions'.")

        name = rule["name"]
        query = rule["query"]
        actions = rule["actions"]

        if not isinstance(name, str):
            raise ValueError(f"Rule name at index {index} must be a string.")
        cleaned_name = name.strip()
        if not cleaned_name:
            raise ValueError(f"Rule name at index {index} must be non-empty.")
        if cleaned_name in seen_rule_names:
            raise ValueError(f"Duplicate rule name found: {cleaned_name}")

        if not isinstance(query, str):
            raise ValueError(f"Rule query for '{cleaned_name}' must be a string.")
        cleaned_query = query.strip()
        if not cleaned_query:
            raise ValueError(f"Rule query for '{cleaned_name}' must be non-empty.")

        if not isinstance(actions, dict):
            raise ValueError(f"Rule actions for '{cleaned_name}' must be an object.")

        add_labels: list[str] = []
        archive = False

        if "add_labels" in actions:
            raw_add_labels = actions["add_labels"]
            if not isinstance(raw_add_labels, list):
                raise ValueError(f"Rule add_labels for '{cleaned_name}' must be a list.")

            for label_index, label_name in enumerate(raw_add_labels):
                if not isinstance(label_name, str):
                    raise ValueError(
                        f"Rule add_labels item at index {label_index} for '{cleaned_name}' must be a string."
                    )

                cleaned_label_name = label_name.strip()
                if not cleaned_label_name:
                    raise ValueError(
                        f"Rule add_labels item at index {label_index} for '{cleaned_name}' must be non-empty."
                    )

                add_labels.append(cleaned_label_name)

        if "archive" in actions:
            archive = actions["archive"]
            if not isinstance(archive, bool):
                raise ValueError(f"Rule archive value for '{cleaned_name}' must be a boolean.")

        if not add_labels and not archive:
            raise ValueError(f"Rule '{cleaned_name}' must define at least one action.")

        seen_rule_names.add(cleaned_name)
        cleaned_rules.append(
            {
                "name": cleaned_name,
                "query": cleaned_query,
                "actions": {
                    "add_labels": add_labels,
                    "archive": archive,
                },
            }
        )

    return cleaned_rules
