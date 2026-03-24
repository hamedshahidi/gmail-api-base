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
      migration_plan_executor.py
      rules_plan_executor.py
      cleanup_plan_executor.py
    services/
      label_management_service.py
      label_service.py
      message_service.py
  docs/
    gmail-organization-plan.md
    development-plan.md
    ai-development-workflow.md
  plans/
    gmail_organization/
      labels.json
      migrations.json
      rules.json
      cleanup.json
      examples/
        labels.example.json
        migrations.example.json
        rules.example.json
        cleanup.example.json
  scripts/
    apply_rules_from_plan.py
    cleanup_labels_from_plan.py
    create_labels_from_plan.py
    migrate_labels_from_plan.py
    list_labels.py
    export_labels.py
  output/
  main.py
  run.sh
  setup_and_run.sh
```

## Architecture

* `gmail_base/` contains reusable core modules.
* `gmail_base/services/` contains reusable Gmail operations.
* `gmail_base/planners/` contains plan loading, validation, and execution logic.
* `scripts/` contains thin entry points.
* `docs/` contains human-readable strategy and development docs.
* `plans/` contains machine-readable execution inputs.
* `output/` contains generated files.
* Message updates use Gmail batch modify for migration efficiency.
* Plans include labels, migrations, rules, and cleanup.
* Rules are generic query-driven automations.
* Cleanup is a safe post-migration label hygiene phase.

## Plan-Driven Approach

* `docs/` explain the strategy and desired direction.
* `plans/` define the executable desired state.
* `plans/gmail_organization/examples/` contains non-executable example plan files for onboarding and future development.
* `scripts/` execute plans through reusable modules.
* Plans are JSON-based (YAML may be added later).
* Rules enable query-based automation.
* Cleanup enables safe removal of legacy labels after migration.

---

## Setup Overview

To run this project, you need to:

1. Create a Google Cloud project
2. Enable the Gmail API
3. Configure the OAuth consent screen
4. Create OAuth credentials as a Desktop app
5. Download `credentials.json` into the project root

---

## Running Scripts

Run directly:

```bash
python scripts/create_labels_from_plan.py
python scripts/migrate_labels_from_plan.py
python scripts/apply_rules_from_plan.py
python scripts/cleanup_labels_from_plan.py
```

Or with helper:

```bash
./run.sh scripts/apply_rules_from_plan.py --apply --verbose
```

---

## Execution Model

### Labels

* Creates missing labels
* Idempotent

### Migration

* Adds new labels
* Does NOT remove old labels

### Rules

* Query-based automation
* Supports labeling and archiving
* Optional `exclude_labels` helps skip already-handled messages
* Reports matched messages and eligible messages after exclusions
* `exclude_labels` belongs at the rule root, not inside `actions`
* Archive = remove `INBOX`

Example:

```json
{
  "name": "example-exclude-already-labeled-receipts",
  "query": "label:\"Kuitti\"",
  "exclude_labels": ["Finance/Receipts"],
  "actions": {
    "add_labels": ["Finance/Receipts"],
    "archive": false
  }
}
```

### Cleanup

* Removes legacy labels
* Requires replacement labels when configured
* Never deletes emails
* Never archives messages

---

## Safety Model

* Preview mode is default
* `--apply` required for execution
* No destructive operations
* Idempotent behavior across all flows

---

## AI-Assisted Development

This project supports a structured AI workflow using Codex and reusable prompt files.

### Key components

* `AGENTS.md` → repository-wide AI rules
* `docs/development-plan.md` → roadmap and architecture
* `.github/prompts/` → reusable task prompts

### Example usage

```text
/implement-next-phase
```

### Creating new prompts

* Keep prompts small
* Do NOT duplicate architecture or plan
* Reference:

  * `AGENTS.md`
  * `docs/development-plan.md`

---

## Detailed AI Workflow

See full guide:

```text
docs/ai-development-workflow.md
```

---

## Important Notes

* Do not commit `credentials.json`
* Do not commit `token.json`
* Keep both files local and private
* If scopes change, delete `token.json` and re-authenticate
