"""Reusable Gmail message search and label modification helpers."""

from __future__ import annotations

from gmail_base.service import get_gmail_service


def search_message_ids(query: str) -> list[str]:
    """Return all Gmail message IDs that match the provided search query."""
    service = get_gmail_service()
    message_ids: list[str] = []
    page_token: str | None = None

    while True:
        response = (
            service.users()
            .messages()
            .list(userId="me", q=query, pageToken=page_token)
            .execute()
        )
        messages = response.get("messages", [])
        message_ids.extend(message["id"] for message in messages if "id" in message)
        page_token = response.get("nextPageToken")

        if not page_token:
            break

    return message_ids


def get_label_name_to_id_map() -> dict[str, str]:
    """Return a mapping of Gmail label names to label IDs."""
    service = get_gmail_service()
    response = service.users().labels().list(userId="me").execute()
    labels = response.get("labels", [])
    return {label["name"]: label["id"] for label in labels if "name" in label and "id" in label}


def add_labels_to_messages(message_ids: list[str], label_ids: list[str]) -> int:
    """Add the provided labels to each message and return the number updated."""
    if not message_ids:
        return 0

    service = get_gmail_service()

    for message_id in message_ids:
        service.users().messages().modify(
            userId="me",
            id=message_id,
            body={"addLabelIds": label_ids},
        ).execute()

    return len(message_ids)
