"""Entry point for Gmail API authentication verification."""

from gmail_base.service import get_gmail_service


def main() -> None:
    """Authenticate with Gmail and print the signed-in email address."""
    service = get_gmail_service()
    profile = service.users().getProfile(userId="me").execute()
    email = profile["emailAddress"]

    print("Authentication successful.")
    print(f"Signed in as: {email}")


if __name__ == "__main__":
    main()
