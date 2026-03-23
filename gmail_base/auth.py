"""OAuth credential loading and refresh helpers for Gmail API access."""

from __future__ import annotations

from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from gmail_base.config import (
    CREDENTIALS_FILE,
    OPEN_BROWSER,
    SCOPES,
    TOKEN_FILE,
)


def get_credentials() -> Credentials:
    """Load, refresh, or create OAuth credentials for the Gmail API."""
    token_path = Path(TOKEN_FILE)
    credentials: Credentials | None = None

    if token_path.exists():
        credentials = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if credentials is None or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            credentials = flow.run_local_server(port=0, open_browser=OPEN_BROWSER)

        token_path.write_text(credentials.to_json(), encoding="utf-8")

    return credentials
