---

mode: agent
description: Refactor Phase 5 rules schema to correctly place exclude_labels at rule level
------------------------------------------------------------------------------------------

Read:

* `AGENTS.md`
* `docs/development-plan.md`

Focus on refining the Phase 5 implementation for rules optimization.

Goal:

* improve schema correctness without changing behavior
* keep implementation minimal and backward compatible

Problem:

* `exclude_labels` is currently placed inside `actions`
* semantically, it is not an action but a rule-level filter

Target design:

Move `exclude_labels` to the rule root level:

{
"name": "example-rule",
"query": "...",
"exclude_labels": ["LabelA"],
"actions": {
"add_labels": [...],
"archive": false
}
}

Requirements:

1. Plan validator

* support `exclude_labels` at the rule root level
* keep it optional
* validate as list[str]
* normalize missing value to []
* remove support from inside `actions` OR support both temporarily (prefer simple if safe)

2. Rules executor

* read `exclude_labels` from rule root
* keep behavior identical:

  * matched = original query
  * eligible = query + exclusions
* do NOT change logic beyond field location

3. Scripts

* update references to `exclude_labels` accordingly
* keep output format unchanged

4. Backward compatibility

* if `exclude_labels` currently exists inside `actions`, either:

  * migrate it cleanly, OR
  * support both locations temporarily (prefer simplest safe option)

5. Constraints

* do NOT introduce new features
* do NOT introduce marker labels
* do NOT change rule behavior
* do NOT add new services
* do NOT over-engineer

6. Documentation

* update README only if necessary (schema change mention)

Keep the change small, clean, and consistent with the existing architecture.
