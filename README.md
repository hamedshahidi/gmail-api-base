# Gmail API Python Base

Minimal Gmail API starter project with reusable Gmail services, plan-driven execution, and thin scripts for safe automation tasks.

## Project Structure

`gmail_base/` contains reusable core modules.
`gmail_base/services/` contains reusable Gmail operations.
`gmail_base/planners/` contains plan loading, validation, and execution logic.
`scripts/` contains thin entry points.
`docs/` contains human-readable strategy and development docs.
`plans/` contains machine-readable execution inputs.
`output/` contains generated files.

```text
gmail-api-base/
  gmail_base/
    config.py
    auth.py
    service.py
    planners/
      plan_loader.py
      plan_validator.py
      label_plan_executor.py
    services/
      label_management_service.py
      label_service.py
  docs/
    gmail-organization-plan.md
    development-plan.md
  plans/
    gmail_organization/
      labels.json
  scripts/
    create_labels_from_plan.py
    list_labels.py
    export_labels.py
  output/
  main.py
  run.sh
  setup_and_run.sh
```

## Architecture

- `gmail_base/` contains reusable core modules.
- `gmail_base/services/` contains reusable Gmail operations.
- `gmail_base/planners/` contains plan loading, validation, and execution logic.
- `scripts/` contains thin entry points.
- `docs/` contains human-readable strategy and development docs.
- `plans/` contains machine-readable execution inputs.
- `output/` contains generated files.

## Plan-Driven Approach

- `docs/` explain the strategy and desired direction.
- `plans/` define the executable desired state.
- `scripts/` execute plans through reusable modules.
- The current machine-readable plan format is JSON.
- YAML may be added later without changing the overall architecture.

## Setup Overview

To run this project, you need to:

1. Create a Google Cloud project
2. Enable the Gmail API
3. Configure the OAuth consent screen
4. Create OAuth credentials as a Desktop app
5. Download `credentials.json` into the project root

## How to get credentials.json

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable Gmail API
4. Configure the OAuth consent screen
5. Create OAuth credentials with application type `Desktop app`
6. Download the JSON file, rename it to `credentials.json`, and place it in the project root

Important:

- The OAuth application type must be `Desktop app`.
- If you see a Gmail API disabled error, enable Gmail API in the selected Google Cloud project.

## Credential Files

- `credentials.json` is downloaded manually from Google Cloud and placed in the project root. This matches `CREDENTIALS_FILE` in `gmail_base/config.py`.
- `token.json` is generated automatically after the first successful authentication. This matches `TOKEN_FILE` in `gmail_base/config.py`.
- `credentials.example.json` and `token.example.json` are reference files only.

## OAuth Scope

This project uses `https://www.googleapis.com/auth/gmail.readonly`.

If you change scopes:

- delete `token.json`
- run authentication again

## Setup on Windows (Git Bash)

You can run setup manually or use the helper scripts.

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

- the app prints a Google auth URL in the terminal
- copy it into Chrome
- sign in
- allow access
- Google redirects to `localhost`
- return to terminal and wait

After success:

- `token.json` is created
- future runs reuse it automatically

## Running Scripts

Run scripts directly:

```bash
python scripts/list_labels.py
python scripts/export_labels.py
python scripts/create_labels_from_plan.py
python scripts/create_labels_from_plan.py plans/gmail_organization/labels.json
```

Or use the helper runner:

```bash
./run.sh scripts/list_labels.py
./run.sh scripts/export_labels.py
./run.sh scripts/create_labels_from_plan.py
./run.sh scripts/create_labels_from_plan.py plans/gmail_organization/labels.json
```

If no argument is passed, `./run.sh` still runs `python main.py`.

## Exported Files

- Exported files go into `output/`.
- The first feature exports Gmail label names to `output/labels.txt`.

## Label Management

Plan-based label creation:

```bash
python scripts/create_labels_from_plan.py
python scripts/create_labels_from_plan.py plans/gmail_organization/labels.json
```

Or:

```bash
./run.sh scripts/create_labels_from_plan.py
./run.sh scripts/create_labels_from_plan.py plans/gmail_organization/labels.json
```

- The plan-driven script only creates missing labels.
- It does not delete or modify existing labels.
- It is safe to run multiple times.

## Existing Label Scripts

- `python scripts/list_labels.py` still lists labels.
- `python scripts/export_labels.py` still exports labels to `output/labels.txt`.

## Helper Scripts

- `setup_and_run.sh` handles first-time setup or reinstalling dependencies.
- `run.sh` activates `.venv` and runs `main.py` by default or any passed Python script path.

Example:

```bash
chmod +x run.sh setup_and_run.sh
./setup_and_run.sh
./run.sh
./run.sh scripts/list_labels.py
./run.sh scripts/export_labels.py
./run.sh scripts/create_labels_from_plan.py
```

## Browser Behavior

- The app does not automatically open a browser.
- The auth URL is printed in the terminal.
- You manually open it in Chrome.
- Google redirects back to `localhost`.
- This avoids changing default browser settings.

## Expected Output

Default auth check:

```text
Authentication successful.
Signed in as: your-email@gmail.com
```

Label export:

```text
Exported labels to: output/labels.txt
```

## Important Notes

- Do not commit `credentials.json`
- Do not commit `token.json`
- Keep both files local and private
- If `token.json` becomes stale or scopes change, delete it and authenticate again
