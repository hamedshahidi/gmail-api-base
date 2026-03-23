"""Execution helpers for label creation plans."""

from __future__ import annotations

from gmail_base.planners.plan_loader import load_label_plan
from gmail_base.services.label_management_service import ensure_labels_exist


def create_labels_from_plan(plan_path: str) -> dict[str, str]:
    """Create missing Gmail labels defined in a machine-readable plan."""
    label_names = load_label_plan(plan_path)
    return ensure_labels_exist(label_names)

