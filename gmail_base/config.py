"""Configuration values for Gmail API authentication."""

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
CREDENTIALS_FILE = "credentials.json"
TOKEN_FILE = "token.json"
# None means use normal/default handling.
BROWSER_NAME = None
# OPEN_BROWSER = False means the app will print the auth URL instead of opening a browser automatically.
OPEN_BROWSER = False
