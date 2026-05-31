# PRD

## Problem

AI collaboration projects fail when task cards omit route, owner, validation, or stop-line information. Future AI dialogues then continue work without knowing whether edits are allowed.

## Users

- A developer starting a new AI-assisted project from the mother package.
- A general AI model that needs a small, evidence-based project to follow.
- A reviewer checking whether a project has traceable execution logic.

## Goal

Provide a minimal offline taskboard validator that demonstrates the mother-package collaboration contract.

## Acceptance Criteria

- A sample taskboard can be loaded from JSON.
- Every task card has required fields.
- At least one validation reference exists per task.
- The smoke test prints `REFERENCE_PROJECT_SMOKE=PASS`.
- Verification requires no API key and no network access.
