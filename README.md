# Gmail API Python Base

Minimal Python base project for Gmail API authentication only. It is intended as a reusable starting point for future Gmail scripts, and for now it only handles:

* signing in with a Google account
* storing the OAuth token locally
* creating a Gmail API service client
* printing the authenticated Gmail address to confirm setup worked

---

## Setup Overview

To run this project, you need to:

1. Create a Google Cloud project
2. Enable the Gmail API
3. Configure the OAuth consent screen
4. Create OAuth credentials (Desktop app)
5. Download `credentials.json` into the project root

---

## How to get credentials.json

1. Go to [Google Cloud Console](https://console.cloud.google.com/)

2. Create a new project or select an existing one

3. Enable Gmail API:

   * Go to **APIs & Services → Library**
   * Search for **Gmail API**
   * Click **Enable**

4. Configure OAuth consent screen:

   * Go to **APIs & Services → OAuth consent screen**
   * Choose **External**
   * Fill required app details and save

5. Create OAuth client:

   * Go to **APIs & Services → Credentials**
   * Click **Create Credentials → OAuth client ID**
   * Choose **Desktop app**
   * Click Create

6. Download credentials:

   * Download the JSON file
   * Rename it to `credentials.json`
   * Place it in the project root

> ⚠️ Important: The OAuth application type must be **Desktop app**.
> Choosing the wrong type will break authentication.

> ⚠️ If you see a "Gmail API has not been used or is disabled" error,
> make sure the Gmail API is enabled in your selected project.

---

## Credential Files

* `credentials.json`
  Downloaded manually from Google Cloud and placed in the project root.
  This matches `CREDENTIALS_FILE` in `gmail_base/config.py`.

* `token.json`
  Generated automatically after the first successful authentication.
  This matches `TOKEN_FILE` in `gmail_base/config.py`.

* `credentials.example.json` and `token.example.json`
  Reference files only — do not use them as real credentials.

---

## OAuth Scope

This project uses:

```
https://www.googleapis.com/auth/gmail.readonly
```

This matches `SCOPES` in `gmail_base/config.py`.

If you change scopes:

* delete `token.json`
* run authentication again

---

## Setup on Windows (Git Bash)

You can either run setup manually or use helper scripts.

### Manual setup

```bash
python -m venv .venv
source .venv/Scripts/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Manual run

```bash
python main.py
```

On first run:

* the app prints a Google auth URL in the terminal
* copy it into Chrome
* sign in
* allow access
* Google redirects to `localhost`
* return to terminal and wait

After success:

* `token.json` is created
* future runs reuse it automatically

---

## Helper Scripts

* `setup_and_run.sh` → first-time setup or reinstall dependencies
* `run.sh` → normal usage

Example:

```bash
chmod +x run.sh setup_and_run.sh
./setup_and_run.sh
./run.sh
```

### Using run.sh

1. Run:

   ```bash
   ./run.sh
   ```
2. Copy the printed URL into Chrome
3. Sign in
4. Let it redirect to `localhost`
5. Return to terminal and wait

---

## Browser Behavior

* The app does **not** automatically open a browser
* The auth URL is printed in the terminal
* You manually open it in Chrome
* Google redirects back to `localhost`
* This avoids changing default browser settings

---

## Expected Output

```text
Authentication successful.
Signed in as: your-email@gmail.com
```

---

## Important Notes

* Do not commit `credentials.json`
* Do not commit `token.json`
* Keep both files local and private
* If `token.json` becomes stale or scopes change, delete it and authenticate again
