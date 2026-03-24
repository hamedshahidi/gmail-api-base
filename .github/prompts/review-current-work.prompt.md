---
mode: agent
description: Review the current uncommitted changes for architecture, safety, and plan alignment
---

Read:
- `AGENTS.md`
- `docs/development-plan.md`

Review the current working tree changes.

Check for:
- architecture consistency
- safety regressions
- broken preview/apply behavior
- unnecessary hardcoding
- backward compatibility issues
- thin-script violations
- missing docs updates
- misleading reporting or logging

Do not implement large new features.
Prefer minimal targeted fixes if needed.

At the end output ONLY:

START_SUMMARY
REVIEW_FINDINGS
<findings>

RECOMMENDED_FIXES
<minimal fixes>

OPTIONAL_PATCHES
<if any>

END_SUMMARY
