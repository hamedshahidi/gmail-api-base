"""Reusable Gmail message search and label modification helpers."""

from __future__ import annotations

from collections.abc import Iterator

from gmail_base.service import get_gmail_service


def chunk_list(items: list[str], size: int) -> Iterator[list[str]]:
    """Yield successive chunks from a list of strings."""
    if size <= 0:
        raise ValueError("Chunk size must be greater than zero.")

    for index in range(0, len(items), size):
        yield items[index : index + size]


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


def add_labels_to_messages(
    message_ids: list[str],
    label_ids: list[str],
    batch_size: int = 1000,
    verbose: bool = False,
) -> int:
    """Add the provided labels to messages in batches and return the number submitted."""
    if not message_ids:
        return 0

    service = get_gmail_service()
    updated_count = 0

    for message_id_chunk in chunk_list(message_ids, batch_size):
        if verbose:
            print(f"Processing batch of {len(message_id_chunk)} messages...", flush=True)

        service.users().messages().batchModify(
            userId="me",
            body={
                "ids": message_id_chunk,
                "addLabelIds": label_ids,
            },
        ).execute()
        updated_count += len(message_id_chunk)

    return updated_count


def archive_messages(
    message_ids: list[str],
    batch_size: int = 1000,
    verbose: bool = False,
) -> int:
    """Archive messages in batches by removing only the INBOX label."""
    if not message_ids:
        return 0

    service = get_gmail_service()
    archived_count = 0

    for message_id_chunk in chunk_list(message_ids, batch_size):
        if verbose:
            print(f"Processing archive batch of {len(message_id_chunk)} messages...", flush=True)

        service.users().messages().batchModify(
            userId="me",
            body={
                "ids": message_id_chunk,
                "removeLabelIds": ["INBOX"],
            },
        ).execute()
        archived_count += len(message_id_chunk)

    return archived_count
