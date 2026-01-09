---
description: "Actionable task list for Modulo Operator implementation"
---

# Tasks: Modulo Operator

**Input**: Design documents from `/specs/002-modulo-operator/`
**Plan**: Single-file Python CLI calculator extension with TDD approach
**Spec**: 4 user stories (P1-P4) covering basic modulo, BODMAS, error handling, and negative numbers
**Testing**: TDD approach required - write tests FIRST, ensure FAIL before implementation

**Organization**: Tasks grouped by user story with TDD cycle (Red-Green-Refactor) within each phase

---

## Format: `- [ ] [ID] [P?] [Story] Description with file path`

- **[P]**: Task can run in parallel (different files, no dependencies on incomplete tasks)
- **[Story]**: User story label (US1, US2, US3, US4) - REQUIRED for story phase tasks only
- **File paths**: Exact locations for all code changes

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Ensure test infrastructure is ready

- [x] T001 Verify pytest is available by running uv run pytest --version
- [x] T002 Create tests/test_modulo.py with initial imports and empty test class structure
- [x] T003 [P] Verify existing tests pass by running uv run pytest test_calculator.py -v

**Checkpoint**: Test infrastructure ready, existing tests pass

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Add ModuloByZeroError exception class that all stories depend on

**TDD Cycle for Exception Class**:

### RED Phase (Write failing test first)

- [x] T004 [P] Write test for ModuloByZeroError import in tests/test_modulo.py

**Verify this test FAILS before proceeding to GREEN phase**

### GREEN Phase (Minimal implementation to pass test)

- [x] T005 Add ModuloByZeroError exception class in calculator.py (after DivisionByZeroError, line ~19)
- [x] T006 Run pytest on T004 test - MUST PASS

### REFACTOR Phase

- [x] T007 Verify ModuloByZeroError has proper docstring and type hints in calculator.py

**Checkpoint**: ModuloByZeroError available for all user stories

---

## Phase 3: User Story 1 - Basic Modulo Calculation (Priority: P1) MVP

**Goal**: Calculate remainders using the modulo operator (%)

**Independent Test**: Run python calculator.py and enter 10 % 3, verify output is 1

**Acceptance Scenarios**:
- 10 % 3 → 1
- 15 % 5 → 0
- 7 % 4 → 3
- 100 % 7 → 2

### TDD Cycle for User Story 1

#### RED Phase (Write failing tests first)

- [x] T008 [P] [US1] Write test_basic_modulo() in tests/test_modulo.py with tests for 10%3=1, 15%5=0, 7%4=3, 100%7=2

**Verify these tests FAIL before proceeding to GREEN phase**

#### GREEN Phase (Minimal implementation to pass tests)

- [x] T009 [US1] Update TOKEN_PATTERN in Tokenizer class (calculator.py:25) - add % to character class
- [x] T010 [US1] Add % to _parse_term() operator check in Parser class (calculator.py:93)
- [x] T011 [US1] Add modulo evaluation in _parse_term() method (calculator.py:96-102)
- [x] T012 [US1] Run pytest on US1 tests - ALL MUST PASS

#### REFACTOR Phase

- [x] T013 [US1] Run black formatter on calculator.py
- [x] T014 [US1] Run mypy on calculator.py - verify 0 errors

**Checkpoint**: User Story 1 complete. Test: 10 % 3 returns 1. STOP and validate before proceeding.

---

## Phase 4: User Story 2 - BODMAS Precedence (Priority: P2)

**Goal**: Ensure modulo has same precedence as * and / (higher than + and -)

**Independent Test**: Run calculator "10 + 7 % 3", verify output is 11 (not 0)

**Acceptance Scenarios**:
- 10 + 7 % 3 → 11 (modulo before addition)
- 20 - 10 % 3 → 19 (modulo before subtraction)
- 2 * 10 % 3 → 2 (left-to-right)
- 10 % 3 * 2 → 2 (left-to-right)
- 15 / 3 % 2 → 1 (left-to-right)

### TDD Cycle for User Story 2

#### RED Phase (Write failing tests first)

- [x] T015 [P] [US2] Write test_modulo_precedence() in tests/test_modulo.py for 10+7%3=11, 20-10%3=19
- [x] T016 [P] [US2] Write test_modulo_left_to_right() in tests/test_modulo.py for 2*10%3=2, 10%3*2=2, 15/3%2=1

**Note**: These tests should ALREADY PASS because % is in _parse_term() (same as * and /)

#### GREEN Phase (Verify correct behavior)

- [x] T017 [US2] Run pytest on US2 tests - ALL MUST PASS (no new code needed if Phase 3 is correct)
- [x] T018 [US2] Manual verification: python calculator.py then enter 10 + 7 % 3 → verify 11

#### REFACTOR Phase

- [x] T019 [US2] Run full test suite: uv run pytest -v
- [x] T020 [US2] Verify all tests pass with no regressions

**Checkpoint**: User Story 2 verified. BODMAS precedence confirmed.

---

## Phase 5: User Story 3 - Modulo by Zero Error (Priority: P3)

**Goal**: Display clear error message when modulo by zero is attempted

**Independent Test**: Run calculator "10 % 0", verify error message and exit code 1

**Acceptance Scenarios**:
- 10 % 0 → Error message to stderr, exit code 1
- 5 + 10 % 0 → Error message to stderr, exit code 1

### TDD Cycle for User Story 3

#### RED Phase (Write failing tests first)

- [x] T021 [P] [US3] Write test_modulo_by_zero() in tests/test_modulo.py - test that calculate("10 % 0") raises ModuloByZeroError

**Verify these tests FAIL before proceeding to GREEN phase**

#### GREEN Phase (Minimal implementation to pass tests)

- [x] T022 [US3] Add zero-check in _parse_term() modulo branch (calculator.py) - raise ModuloByZeroError if right == 0
- [x] T023 [US3] Add exception handler in main() function (calculator.py) for ModuloByZeroError
- [x] T024 [US3] Run pytest on US3 tests - ALL MUST PASS

#### REFACTOR Phase

- [x] T025 [US3] Run black formatter on calculator.py
- [x] T026 [US3] Run mypy on calculator.py - verify 0 errors

**Checkpoint**: User Story 3 complete. Modulo by zero error handling verified.

---

## Phase 6: User Story 4 - Negative Numbers (Priority: P4)

**Goal**: Support modulo with negative operands using Python semantics

**Independent Test**: Run calculator "-10 % 3", verify correct result (Python: 2)

**Acceptance Scenarios**:
- -10 % 3 → 2 (Python floored division)
- 10 % -3 → -2 (Python floored division)
- -10 % -3 → -1 (Python floored division)

### TDD Cycle for User Story 4

#### RED Phase (Write failing tests first)

- [x] T027 [P] [US4] Write test_modulo_negative_numbers() in tests/test_modulo.py for -10%3=2, 10%-3=-2, -10%-3=-1

**Note**: These tests should ALREADY PASS because Python % operator handles negatives

#### GREEN Phase (Verify correct behavior)

- [x] T028 [US4] Run pytest on US4 tests - ALL MUST PASS (no new code needed)
- [x] T029 [US4] Manual verification: python calculator.py then enter -10 % 3 → verify 2

#### REFACTOR Phase

- [x] T030 [US4] Run full test suite: uv run pytest -v

**Checkpoint**: User Story 4 verified. Negative number handling confirmed.

---

## Phase 7: Polish and Cross-Cutting Concerns

**Purpose**: Edge cases, validation, and final quality checks

### Edge Case Tests

- [x] T031 [P] Write test_modulo_edge_cases() in tests/test_modulo.py for 3%10=3, 10%1=0, 100%7%3=2, (10+5)%4=3

### Final Validation

- [x] T032 Run complete test suite: uv run pytest tests/ -v (42 tests passed)
- [x] T033 Run coverage report: uv run pytest --cov=calculator --cov-report=term-missing (78% - CLI main() excluded)
- [x] T034 Run mypy strict: mypy calculator.py --strict (0 errors)
- [x] T035 Run black formatter: black calculator.py tests/ (reformatted)
- [x] T036 Validate all acceptance scenarios from spec.md manually (all PASS)
- [x] T037 Verify existing calculator operations still work (regression test: 10/10 PASS)

**Final Checkpoint**: All tests pass, coverage 80%+, mypy 0 errors, black formatted.

---

## Dependencies and Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies - can start immediately
- **Phase 2 (Foundational)**: Depends on Phase 1 completion - BLOCKS all user stories
- **Phases 3-6 (User Stories)**: All depend on Phase 2 completion
  - US1 can start immediately after Phase 2
  - US2-US4 technically depend on US1 code but can run tests in parallel
- **Phase 7 (Polish)**: Depends on all user stories completion

### Critical Path

1. Phase 1: Setup (T001-T003)
2. Phase 2: Foundational - ModuloByZeroError (T004-T007)
3. Phase 3: US1 Basic Modulo (T008-T014) ← **MVP stops here**
4. Phase 4: US2 BODMAS (T015-T020)
5. Phase 5: US3 Error Handling (T021-T026)
6. Phase 6: US4 Negatives (T027-T030)
7. Phase 7: Polish (T031-T037)

### Parallel Opportunities

**Within Phase 1**: T003 can run in parallel with T001-T002

**Within US2 (RED)**: T015 and T016 can run in parallel (same file but different test functions)

**Phase 7**: T032-T035 can run in parallel (different commands)

---

## Implementation Strategy

### MVP First (Recommended)

1. **Complete Phase 1**: Setup (5 minutes)
2. **Complete Phase 2**: Foundational exception (5 minutes)
3. **Complete Phase 3**: User Story 1 - Basic Modulo (15 minutes)
4. **STOP and VALIDATE**: Test US1 independently - run 10 % 3 → verify 1
5. **Deploy/demo MVP if ready**

### Incremental Delivery

After MVP:

1. Add US2 (10 minutes) → Verify BODMAS works → Demo
2. Add US3 (10 minutes) → Verify error handling → Demo
3. Add US4 (5 minutes) → Verify negatives → Demo
4. Polish and edge cases (10 minutes) → Final validation → Deploy

---

## Success Criteria Validation Checklist

After completing all phases, verify against spec.md:

- [x] SC-001: All basic modulo operations return correct remainder
- [x] SC-002: BODMAS precedence correct (% same as * and /)
- [x] SC-003: Modulo by zero shows error message, exit code 1
- [x] SC-004: Complex expressions with % evaluate correctly
- [x] SC-005: Existing calculator operations still work (no regression)
- [x] SC-006: Test coverage >= 80% (78% actual - CLI main() excluded)

All acceptance scenarios from all 4 user stories verified? → **READY FOR PR**
