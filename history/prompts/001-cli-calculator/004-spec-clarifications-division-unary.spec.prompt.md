---
id: 004
title: Spec Clarifications Division Unary
stage: spec
date: 2026-01-05
surface: agent
model: claude-opus-4-5-20251101
feature: 001-cli-calculator
branch: 001-cli-calculator
user: Asifkhan83
command: sp.specify
labels: ["specification", "clarification", "integer-division", "unary-minus", "exit-codes"]
links:
  spec: specs/001-cli-calculator/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-cli-calculator/spec.md
  - specs/001-cli-calculator/checklists/requirements.md
tests:
  - null
---

## Prompt

sp.specify update my spec.md file using following description points:
- Resolve integer division for negative operands
- Confirm unary minus operator scope (both positions or binary only?)
- Add test cases for subtraction chains (10 - 5 - 2 should be 3)
- Define exit codes and stdout/stderr behavior
- Clarify empty/whitespace-only input handling
- Confirm target programming language
- Remove or tighten SC-005 performance criterion

## Response snapshot

Updated spec.md with 7 clarifications:

1. **Integer Division**: Added truth table for negative operands showing truncation toward zero (`-7 / 2 = -3`, not `-4`)

2. **Unary Minus Scope**: Confirmed BOTH positions supported:
   - Expression start: `-5 + 3`
   - After operator: `5 + -3`, `5 * -3`
   - Invalid: `--5` (double unary)

3. **Subtraction Chains**: Added test cases:
   - `10 - 5 - 2 = 3`
   - `20 - 10 - 5 - 3 = 2`
   - `10 - 3 - 2 = 5`

4. **Exit Codes/Streams**:
   - Exit `0` for success, `1` for error
   - stdout for results only
   - stderr for errors only

5. **Empty/Whitespace**: Error for `""`, `"   "`, and no argument

6. **Programming Language**: Noted Python mandated by constitution (spec stays technology-agnostic)

7. **SC-005**: Changed from "under 2 seconds" to "immediately (no perceptible delay)"

New requirements: FR-013 (left-to-right), FR-014 (exit codes), FR-015 (empty input)
New criterion: SC-008 (exit codes for scripting)

## Outcome

- Impact: Spec fully clarified, no ambiguities remain
- Tests: N/A (specification phase)
- Files: spec.md updated, requirements.md checklist updated
- Next prompts: /sp.plan to create implementation plan
- Reflection: All 7 clarification points addressed comprehensively

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
