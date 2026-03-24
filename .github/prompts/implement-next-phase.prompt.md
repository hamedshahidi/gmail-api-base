---
mode: agent
description: Inspect the repo, read the development plan, and implement the next meaningful phase cleanly and safely
---

Read:
- `AGENTS.md`
- `docs/development-plan.md`

Then:

1. Inspect the current repository and determine what is already implemented versus what is still missing or weak relative to the development plan.
2. Identify the next meaningful implementation step from the plan.
3. Prefer the smallest clean change that moves the project forward.
4. Preserve preview-first safety and backward compatibility.
5. Keep scripts thin and business logic in planners/services.
6. Update docs only if behavior or supported plan capabilities changed.

Priorities:
- First continue the highest-priority incomplete phase from the development plan.
- If a phase is partially complete, refine it before jumping ahead.
- Prefer practical improvements over speculative architecture.

Before finishing:
- verify imports and paths
- verify scripts still work with default plan paths
- verify preview remains the default
- verify existing labels/migrations/rules/cleanup flows are not broken

At the end output ONLY:

START_SUMMARY
UPDATED_FILES
<list of all created/changed files>

PROJECT_TREE
<updated relevant project tree>

WHAT_CHANGED
<concise but useful summary of what was implemented and why>

GIT_DIFF
<full git diff>

NOTES
<any important validation decisions, compatibility notes, or recommended follow-up steps>

END_SUMMARY
