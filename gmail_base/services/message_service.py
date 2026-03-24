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


def get_messages_metadata(
    message_ids: list[str],
    metadata_headers: list[str] | None = None,
    batch_size: int = 100,
) -> list[dict]:
    """Return Gmail message metadata for the provided message IDs."""
    if not message_ids:
        return []

    service = get_gmail_service()
    messages_metadata: list[dict] = []
    metadata_headers = metadata_headers or []

    for message_id_chunk in chunk_list(message_ids, batch_size):
        chunk_results: dict[str, dict] = {}
        chunk_errors: dict[str, Exception] = {}

        def handle_response(request_id: str, response: dict, exception: Exception | None) -> None:
            if exception is not None:
                chunk_errors[request_id] = exception
                return

            chunk_results[request_id] = response

        batch_request = service.new_batch_http_request(callback=handle_response)

        for message_id in message_id_chunk:
            request = service.users().messages().get(
                userId="me",
                id=message_id,
                format="metadata",
                metadataHeaders=metadata_headers,
            )
            batch_request.add(request, request_id=message_id)

        batch_request.execute()

        if chunk_errors:
            failed_message_ids = ", ".join(sorted(chunk_errors))
            error_details = "; ".join(
                f"{message_id}: {chunk_errors[message_id]}"
                for message_id in sorted(chunk_errors)
            )
            raise RuntimeError(
                f"Failed to fetch Gmail message metadata for: {failed_message_ids}. "
                f"Errors: {error_details}"
            )

        for message_id in message_id_chunk:
            if message_id in chunk_results:
                messages_metadata.append(chunk_results[message_id])

    return messages_metadata


def get_label_name_to_id_map() -> dict[str, str]:
    """Return a mapping of Gmail label names to label IDs."""
    service = get_gmail_service()
    response = service.users().labels().list(userId="me").execute()
    labels = response.get("labels", [])
    return {label["name"]: label["id"] for label in labels if "name" in label and "id" in label}


def batch_modify_message_labels(
    message_ids: list[str],
    add_label_ids: list[str] | None = None,
    remove_label_ids: list[str] | None = None,
    batch_size: int = 1000,
    verbose: bool = False,
) -> int:
    """Modify Gmail message labels in batches and return the number submitted."""
    if not message_ids:
        return 0

    service = get_gmail_service()
    updated_count = 0
    add_label_ids = add_label_ids or []
    remove_label_ids = remove_label_ids or []

    for message_id_chunk in chunk_list(message_ids, batch_size):
        if verbose:
            print(f"Processing batch of {len(message_id_chunk)} messages...", flush=True)

        service.users().messages().batchModify(
            userId="me",
            body={
                "ids": message_id_chunk,
                "addLabelIds": add_label_ids,
                "removeLabelIds": remove_label_ids,
            },
        ).execute()
        updated_count += len(message_id_chunk)

    return updated_count


def add_labels_to_messages(
    message_ids: list[str],
    label_ids: list[str],
    batch_size: int = 1000,
    verbose: bool = False,
) -> int:
    """Add the provided labels to messages in batches and return the number submitted."""
    return batch_modify_message_labels(
        message_ids,
        add_label_ids=label_ids,
        batch_size=batch_size,
        verbose=verbose,
    )


def archive_messages(
    message_ids: list[str],
    batch_size: int = 1000,
    verbose: bool = False,
) -> int:
    """Archive messages in batches by removing only the INBOX label."""
    return batch_modify_message_labels(
        message_ids,
        remove_label_ids=["INBOX"],
        batch_size=batch_size,
        verbose=verbose,
    )
