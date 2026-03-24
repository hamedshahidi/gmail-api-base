"""Reusable Gmail message search and label modification helpers."""

from __future__ import annotations

import time
from collections.abc import Iterator
from concurrent.futures import ThreadPoolExecutor, as_completed

from googleapiclient.errors import HttpError

from gmail_base.service import get_gmail_service


def _fetch_message_metadata_with_retry(
    message_id: str,
    metadata_headers: list[str] | None = None,
    max_retries: int = 5,
    base_delay: float = 0.5,
) -> dict:
    """
    Fetch a single message's metadata with retry logic for rate limit errors.
    
    Detects HTTP 429 (rateLimitExceeded) and retries with exponential backoff.
    On persistent failure, raises RuntimeError with the message ID.
    
    Args:
        message_id: Gmail message ID to fetch
        metadata_headers: Optional list of metadata headers to include
        max_retries: Number of retry attempts (default: 5)
        base_delay: Initial delay in seconds before retry (default: 0.5)
    
    Returns:
        Message metadata dictionary
    
    Raises:
        RuntimeError: If all retries are exhausted
    """
    service = get_gmail_service()
    metadata_headers = metadata_headers or []
    attempt = 0
    
    while attempt <= max_retries:
        try:
            response = service.users().messages().get(
                userId="me",
                id=message_id,
                format="metadata",
                metadataHeaders=metadata_headers,
            ).execute()
            return response
        except HttpError as exc:
            # Check for rate limit error (429)
            if exc.resp.status == 429:
                if attempt < max_retries:
                    # Exponential backoff with small jitter
                    delay = base_delay * (2 ** attempt)
                    time.sleep(delay)
                    attempt += 1
                    continue
                else:
                    # All retries exhausted
                    raise RuntimeError(
                        f"Failed to fetch metadata for message {message_id} after {max_retries} retries. "
                        f"Rate limit exceeded. Last error: {exc}"
                    ) from exc
            else:
                # Non-rate-limit errors fail immediately
                raise RuntimeError(
                    f"Failed to fetch metadata for message {message_id}. "
                    f"Error: {exc}"
                ) from exc
        except Exception as exc:
            # Unexpected errors fail immediately
            raise RuntimeError(
                f"Failed to fetch metadata for message {message_id}. "
                f"Unexpected error: {exc}"
            ) from exc
    
    # Should not reach here, but raise if it does
    raise RuntimeError(f"Failed to fetch metadata for message {message_id}. Unknown error.")


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
    """
    Return Gmail message metadata for the provided message IDs.
    
    Uses bounded concurrency to avoid overwhelming the Gmail API.
    Implements retry logic with exponential backoff for rate limit errors.
    
    Args:
        message_ids: List of Gmail message IDs to fetch
        metadata_headers: Optional list of metadata headers to include
        batch_size: Number of messages to fetch per concurrent batch (default: 100)
    
    Returns:
        List of message metadata dictionaries in the order of input message IDs
    
    Raises:
        RuntimeError: If any message fetch fails after retries
    """
    if not message_ids:
        return []

    metadata_headers = metadata_headers or []
    messages_metadata: list[dict] = []
    
    # Use bounded concurrency to avoid rate limits
    # max_workers=10 gives us 10 concurrent requests at a time
    max_workers = 10
    inter_chunk_delay = 0.5  # Small delay between chunks to avoid bursts
    
    # Process messages in chunks with concurrency control
    for chunk_num, message_id_chunk in enumerate(chunk_list(message_ids, batch_size)):
        # Add small delay between chunks (except for the first chunk)
        if chunk_num > 0:
            time.sleep(inter_chunk_delay)
        
        # Use thread pool for this chunk with bounded concurrency
        chunk_results: dict[str, dict] = {}
        chunk_failures: dict[str, RuntimeError] = {}
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all fetch tasks for this chunk
            future_to_message_id = {
                executor.submit(
                    _fetch_message_metadata_with_retry,
                    msg_id,
                    metadata_headers,
                ): msg_id
                for msg_id in message_id_chunk
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_message_id):
                message_id = future_to_message_id[future]
                try:
                    metadata = future.result()
                    chunk_results[message_id] = metadata
                except RuntimeError as exc:
                    chunk_failures[message_id] = exc
        
        # Check for any failures in this chunk
        if chunk_failures:
            failed_message_ids = ", ".join(sorted(chunk_failures.keys()))
            error_details = "; ".join(
                f"{msg_id}: {chunk_failures[msg_id]}"
                for msg_id in sorted(chunk_failures)
            )
            raise RuntimeError(
                f"Failed to fetch Gmail message metadata for {len(chunk_failures)} "
                f"message(s) in chunk: {failed_message_ids}. "
                f"Details: {error_details}"
            )
        
        # Append results in the order of the input chunk
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

        try:
            service.users().messages().batchModify(
                userId="me",
                body={
                    "ids": message_id_chunk,
                    "addLabelIds": add_label_ids,
                    "removeLabelIds": remove_label_ids,
                },
            ).execute()
        except Exception as exc:
            chunk_message_ids = ", ".join(message_id_chunk)
            raise RuntimeError(
                f"Failed to modify Gmail message labels for: {chunk_message_ids}. Error: {exc}"
            ) from exc
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
