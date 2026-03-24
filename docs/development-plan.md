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
* plan-driven label creation
* Phase 2 migration execution
* Phase 3 query-driven rules execution
* Phase 4 plan-driven label cleanup

Current weaknesses:

* some scripts are still repetitive in structure
* rules may reprocess already-handled emails unless queries avoid them
* cleanup previews may be slower on larger mailboxes
* reporting is useful but still basic
* long-term optimization path is not yet formalized

---

## Target Architecture

### Core modules

gmail_base/

* services → reusable Gmail API operations
* planners → plan loading, validation, execution
* models → optional shared structures

No business logic or personal rules inside reusable modules.

---

### Scripts

scripts/

Thin entry points only.

* no business logic
* call planners/services
* accept plan paths
* preview mode is default

---

### Plans

docs → human-readable strategy
plans → machine-readable execution

plans/gmail_organization/

* labels.json
* migrations.json
* rules.json
* cleanup.json

---

## Design Principles

* plan-driven system
* safe by default (preview first)
* idempotent operations
* no destructive actions
* separation of concerns
* generic, reusable components
* no hardcoded behavior

---

## Execution Model

### Labels

create missing labels from labels.json
safe to rerun

---

### Migration

add new labels to messages
do NOT remove old labels
preview by default

---

### Rules

query-based automation

supports:

* add_labels
* root-level eligibility filtering such as exclude_labels
* archive (remove INBOX)

rules are:

* plan-driven
* safe to rerun
* preview-first

---

### Cleanup

remove legacy labels safely

rules:

* only remove specified labels
* require replacement labels when defined
* never delete emails
* never archive emails
* preview-first

---

## Archiving (Important)

Archiving is a first-class feature:

* archive = remove INBOX label
* must be explicitly defined in rules.json
* never implicit
* never part of cleanup or migration

---

## Safety Requirements

Must never:

* delete emails
* remove labels automatically without plan
* commit credentials or sensitive data

Must always:

* default to preview mode
* require explicit apply
* keep operations idempotent
* separate cleanup from migration

---

## Implementation Phases

### Phase 1 — Labels

✅ complete

---

### Phase 2 — Migration

✅ complete

---

### Phase 3 — Rules

✅ complete

* add labels
* archive support
* batch processing

---

### Phase 4 — Cleanup

✅ complete

* safe label removal
* requires validation
* batch processing

---

### Phase 5 — Rules Optimization

✅ complete

Goal:
avoid unnecessary reprocessing

Approaches:

* improve queries to skip already-processed emails
* initial step implemented: optional `exclude_labels`
* optional marker-label strategy
* better reporting (matched vs eligible vs submitted)

---

### Phase 6 — Performance & Reporting

✅ complete

* optimize metadata-heavy operations
* improve logs and summaries
* maintain same behavior with better efficiency

---

### Phase 7 — Orchestration

✅ complete

* initial step implemented: optional unified CLI runner for labels, migrations, rules, and cleanup
* initial step implemented: optional pipeline runner using default plan paths for labels → migrations → rules → cleanup, with labels skipped unless apply is explicit
* initial step implemented: optional pipeline plan-directory override for running the orchestration flow against a different plan set
* optional unified CLI
* optional pipeline:
  labels → migrations → rules → cleanup
* still allow independent execution

---

### Phase 8 — Plan Evolution

* initial step implemented: optional extension-based plan loading for `.json`, `.yaml`, and `.yml`
* YAML support is optional and requires PyYAML when YAML plan files are used
* YAML path has been validated in practical usage and examples for labels, rules, and cleanup
* optional YAML support
* no breaking changes
* keep plan-driven architecture

---

## Success Criteria

* all phases run from JSON plans
* preview is default everywhere
* archive works as explicit rule action
* cleanup only removes intended labels
* scripts remain thin
* services remain generic
* system is safe to rerun
* no secrets or generated data committed
* new features extend plans, not scripts
