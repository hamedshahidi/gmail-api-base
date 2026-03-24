# AI Development Workflow

## Overview

This project uses an **AI-assisted development workflow** built around:

* Codex / AI agents in VS Code
* reusable prompt files
* repository-level instructions
* a plan-driven architecture

The goal is to:

* avoid repeating long prompts
* enforce consistent architecture decisions
* keep development safe, structured, and scalable
* enable fast iteration without losing control

---

## Core Concept

Instead of writing long prompts every time, the project separates AI guidance into **three layers**:

### 1. AGENTS.md (Global Rules)

This file defines how the AI should behave inside the repository.

It includes:

* architecture rules
* safety constraints
* development principles
* output format requirements

Think of it as a **persistent system prompt for the repo**.

---

### 2. Development Plan (Roadmap)

File:

```
docs/development-plan.md
```

This defines:

* project goals
* architecture
* phases
* current state
* future direction

AI agents must treat this as the **source of truth** for what to build next.

---

### 3. Prompt Files (Reusable Tasks)

Location:

```
.github/prompts/
```

These are **reusable commands** for Codex / VS Code.

Each file defines a task like:

* implement next phase
* review changes
* implement a specific feature

---

## Folder Structure

```text
AGENTS.md
README.md

docs/
  development-plan.md
  ai-development-workflow.md

.github/
  prompts/
    implement-next-phase.prompt.md
    review-current-work.prompt.md
```

---

## How It Works

### Step 1 — AI reads instructions

Every time you run a prompt:

* AI reads `AGENTS.md`
* AI reads `docs/development-plan.md`
* AI reads your prompt file

This replaces the need to paste long prompts manually.

---

### Step 2 — AI inspects the repository

The AI must:

* understand current implementation
* compare it with the development plan
* detect gaps or improvements

---

### Step 3 — AI makes targeted changes

The AI should:

* implement only what is needed
* avoid rewriting working code
* preserve architecture
* follow safety rules

---

### Step 4 — AI outputs structured summary

All implementation prompts must end with:

```
START_SUMMARY
...
END_SUMMARY
```

This ensures:

* clean diffs
* easy review
* reproducible changes

---

## Using Prompt Files in VS Code

Prompt files live in:

```
.github/prompts/
```

They can be invoked inside Codex chat using:

```
/prompt-name
```

Example:

```
/implement-next-phase
```

---

## Default Prompt

### implement-next-phase

This is the main reusable development prompt.

It tells the AI to:

* read the repo
* read the development plan
* implement the next logical step
* keep everything safe and clean

Use it for general progress:

```
/implement-next-phase
```

---

## Creating Task-Specific Prompts

Only create a new prompt when:

* a task is repeated
* the logic becomes complex
* you want consistent behavior across runs

---

### Example: Phase-specific prompt

File:

```
.github/prompts/phase-5-rules-optimization.prompt.md
```

Example content:

```md
---
mode: agent
description: Implement Phase 5 rules optimization
---

Read:
- AGENTS.md
- docs/development-plan.md

Focus on Phase 5 only.

Goals:
- reduce unnecessary reprocessing
- preserve plan-driven design
- keep preview/apply behavior intact

Before finishing:
- verify imports
- verify scripts still work

Output:
START_SUMMARY
...
END_SUMMARY
```

---

## Best Practices

### 1. Keep prompts small

Do NOT repeat:

* architecture
* safety rules
* development plan

These already exist in:

* AGENTS.md
* development-plan.md

---

### 2. Prefer generic over specific

Avoid:

* hardcoded labels
* hardcoded queries
* one-off logic

Always:

* extend plans
* extend planners/services

---

### 3. Preserve safety model

Always ensure:

* preview mode is default
* apply mode is explicit
* no destructive behavior
* cleanup is safe

---

### 4. Keep scripts thin

Scripts must:

* call planners/services
* not contain business logic

---

### 5. Maintain backward compatibility

When extending plans:

* never break existing JSON structure
* use optional fields
* validate clearly

---

## Development Workflow

### Normal development

```
/implement-next-phase
```

---

### Feature-specific work

```
/phase-5-rules-optimization
```

---

### Review before commit

```
/review-current-work
```

---

## When to Update Files

### Update AGENTS.md when:

* architecture rules change
* safety model changes
* coding standards evolve

---

### Update development-plan.md when:

* new phase is added
* roadmap changes
* architecture evolves

---

### Update prompt files when:

* workflow improves
* repeated tasks emerge
* new reusable patterns appear

---

## What NOT to Do

Do NOT:

* paste long prompts every time
* duplicate the development plan inside prompts
* bypass planners/services
* add unsafe operations
* break existing flows

---

## Future Improvements

Possible future enhancements:

* unified CLI orchestration
* scheduled automation
* YAML plan support
* smarter rule processing
* performance optimizations

---

## Summary

This workflow enables:

* consistent development
* reusable AI prompts
* safer automation
* scalable architecture

The key idea:

**Move knowledge into the repository, not into prompts.**

Then keep prompts minimal, reusable, and focused.
