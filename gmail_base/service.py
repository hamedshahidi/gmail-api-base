"""Factory for creating an authenticated Gmail API service client."""

from __future__ import annotations

from googleapiclient.discovery import Resource, build

from gmail_base.auth import get_credentials


def get_gmail_service() -> Resource:
    """Create and return an authenticated Gmail API service client."""
    credentials = get_credentials()
    return build("gmail", "v1", credentials=credentials)
