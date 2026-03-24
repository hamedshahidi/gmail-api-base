# AGENTS.md

## Project identity

This repository is a Python-based Gmail automation framework built around a plan-driven architecture.

The system must remain:
- generic
- reusable
- safe by default
- preview-first for modifying workflows
- maintainable and scalable

## Core architecture rules

- `gmail_base/services/` contains low-level reusable Gmail API operations.
- `gmail_base/planners/` contains plan loading, validation, and execution logic.
- `scripts/` must remain thin entry points only.
- `plans/` contains machine-readable execution inputs.
- `docs/` contains human-readable design and strategy.

Do not put personal Gmail workflow logic into reusable Python modules.

## Working style

Before making changes:
1. Inspect the repository and determine what is already implemented.
2. Compare the current codebase against `docs/development-plan.md`.
3. Implement only what is missing, broken, or clearly needs refinement.
4. Preserve existing working functionality.
5. Prefer small, clean, production-quality changes.

Do not rewrite the project from scratch unless explicitly asked.

## Safety rules

- Preview mode must remain the default for modifying workflows.
- Apply mode must always be explicit.
- Do not add email deletion behavior.
- Do not add destructive label deletion behavior unless explicitly requested and designed safely.
- Cleanup must stay separate from migration.
- Archive is allowed only as an explicit rule action and means removing `INBOX`.

## Design rules

- Keep the system plan-driven.
- Do not hardcode labels, queries, or user-specific workflows in Python.
- Prefer generic reusable methods over one-off helpers.
- Keep code typed where reasonable.
- Preserve backward compatibility with existing JSON plans whenever possible.
- If you extend a plan schema, make it backward compatible and validate it clearly.

## Documentation rules

- Update `README.md` when behavior, usage, or plan schema changes.
- Update `docs/development-plan.md` only when the architectural plan or roadmap materially changes.
- Do not rewrite docs unnecessarily.

## Output rules for larger implementation tasks

When asked to implement or update the repo, output a single plain-text summary block in this structure unless a prompt explicitly defines a different output format:

START_SUMMARY
UPDATED_FILES
<list>

PROJECT_TREE
<relevant tree>

WHAT_CHANGED
<summary>

GIT_DIFF
<full git diff>

NOTES
<notes>

END_SUMMARY

Do not wrap that final summary in markdown fences unless explicitly asked.
