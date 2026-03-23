# Gmail API Base — Development Plan

## Goal

Evolve the project from a working Gmail API authentication base into a reusable, plan-driven Gmail automation toolkit.

The system must:

* keep authentication and raw Gmail client access reusable
* support generic reusable services
* avoid hardcoded personal logic in scripts
* execute automation tasks from machine-readable input files
* keep human-readable strategy and machine-readable execution inputs separate
* remain safe by default

---

## Current State

The project already supports:

* Gmail OAuth authentication
* authenticated Gmail service creation
* helper runner scripts
* listing labels
* exporting labels
* creating a planned label hierarchy

Current weaknesses:

* some scripts are task-specific
* parts of the logic are hardcoded to the current Gmail organization plan
* generated files must be managed carefully
* the project needs a more explicit architecture for reusable automation

---

## Target Architecture

### 1. Core modules

`gmail_base/` should contain reusable code only.

```text
gmail_base/
  config.py
  auth.py
  service.py

  services/
    label_service.py
    label_management_service.py
    message_service.py
    search_service.py

  planners/
    __init__.py
    plan_loader.py
    plan_validator.py
    label_plan_executor.py
    migration_plan_executor.py

  models/
    __init__.py
    plan_models.py
```

Principles:

* `services/` = low-level reusable Gmail operations
* `planners/` = plan loading, validation, and execution logic
* `models/` = shared typed structures if needed later
* no personal Gmail plan should be hardcoded inside reusable modules

---

### 2. Scripts

`scripts/` should remain thin entry points only.

```text
scripts/
  list_labels.py
  export_labels.py
  create_labels_from_plan.py
  validate_plan.py
  migrate_labels_from_plan.py
```

Principles:

* scripts call services/planners
* scripts contain no business logic
* scripts accept plan file paths

---

### 3. Plans

Separate human intent from machine execution.

#### Human-readable documentation

```text
docs/
  gmail-organization-plan.md
  development-plan.md
```

#### Machine-readable execution inputs

```text
plans/
  gmail_organization/
    labels.json
    migrations.json
    filters.json
```

Principles:

* docs explain *why*
* plans define *what*
* code defines *how*

---

## Design Principles

1. Authentication stays generic
2. Gmail operations stay generic
3. Scripts remain thin
4. Plans are data, not code
5. Human-readable strategy and machine-readable inputs are separate
6. Safe defaults:

   * create before modify
   * do not delete labels automatically
   * do not remove old labels until verified
7. Generated files go to `output/` and are ignored
8. System should be idempotent

---

## Input Format Strategy

Use **JSON for now** (no external dependencies).
Design in a way that allows switching to YAML later.

### labels.json

```json
{
  "labels": [
    "Finance",
    "Finance/Bank",
    "Finance/Salary"
  ]
}
```

### migrations.json

```json
{
  "migrations": [
    {
      "old_label": "visa",
      "new_labels": ["Finance/Bank"]
    }
  ]
}
```

### filters.json (future)

```json
{
  "rules": [
    {
      "name": "receipts",
      "query": "subject:(receipt OR kuitti)",
      "actions": {
        "add_labels": ["Finance/Receipts"],
        "archive": false
      }
    }
  ]
}
```

---

## Execution Model

### Label creation

Script:

```
scripts/create_labels_from_plan.py
```

Behavior:

* load labels.json
* validate
* create missing labels
* safe to re-run

---

### Migration

Script:

```
scripts/migrate_labels_from_plan.py
```

Behavior:

* load migrations.json
* apply new labels
* DO NOT remove old labels initially

---

### Validation

Script:

```
scripts/validate_plan.py
```

Behavior:

* validate JSON structure
* detect duplicates
* check references

---

## Required Project Changes

### 1. Add planners package

* plan_loader.py
* plan_validator.py
* label_plan_executor.py

### 2. Move hardcoded data to JSON

* no label lists inside scripts

### 3. Replace task-specific script

* remove create_planned_labels.py
* add create_labels_from_plan.py

### 4. Keep generic scripts

* list_labels.py
* export_labels.py

### 5. Update README

Explain:

* architecture
* plans vs docs
* how to run plan scripts

### 6. Improve .gitignore

```gitignore
output/*
!output/.gitkeep
```

---

## Safety Requirements

Must never:

* commit credentials.json
* commit token.json
* commit exported Gmail data

Must:

* avoid destructive operations
* avoid deleting labels automatically
* avoid removing old labels prematurely

---

## Implementation Phases

### Phase 1 — Plan-driven label creation

* JSON label plan
* loader + validator
* generic script
* README update

### Phase 2 — Migration engine

* migrations.json
* migration executor
* reporting

### Phase 3 — Search & rules

* search service
* filter plan

### Phase 4 — CLI (optional)

* unify commands

---

## Immediate Next Step

Implement Phase 1:

* planners package
* labels.json
* generic label creation script
* README update

---

## Success Criteria

Phase 1 is complete when:

* no label data is hardcoded
* labels are loaded from JSON
* validation exists
* script is reusable
* README explains usage
* secrets and outputs are not tracked
