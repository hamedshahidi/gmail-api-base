"""Helpers for creating Gmail labels safely."""

from __future__ import annotations

from gmail_base.service import get_gmail_service


def list_existing_labels() -> list[dict]:
    """Return all existing labels for the authenticated Gmail account."""
    service = get_gmail_service()
    response = service.users().labels().list(userId="me").execute()
    return response.get("labels", [])


def get_existing_label_names() -> set[str]:
    """Return the names of all existing labels for the authenticated account."""
    return {label["name"] for label in list_existing_labels() if "name" in label}


def create_label(label_name: str) -> dict:
    """Create a Gmail label with the default visible settings."""
    service = get_gmail_service()
    body = {
        "name": label_name,
        "messageListVisibility": "show",
        "labelListVisibility": "labelShow",
    }
    return service.users().labels().create(userId="me", body=body).execute()


def ensure_labels_exist(label_names: list[str]) -> dict[str, str]:
    """Ensure each requested label exists and return its creation status."""
    existing_label_names = get_existing_label_names()
    status_by_label: dict[str, str] = {}

    for label_name in label_names:
        if label_name in status_by_label:
            continue

        if label_name in existing_label_names:
            status_by_label[label_name] = "exists"
            continue

        create_label(label_name)
        existing_label_names.add(label_name)
        status_by_label[label_name] = "created"

    return status_by_label
