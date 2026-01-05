---
description: "Actionable task list for CLI Calculator implementation"
---

# Tasks: CLI Calculator

**Input**: Design documents from `/specs/001-cli-calculator/`
**Plan**: Single-file Python CLI calculator with recursive descent parser, BODMAS precedence, integer division, error handling
**Spec**: 4 user stories (P1-P4) covering basic arithmetic, BODMAS, error handling, and input validation
**Testing**: TDD approach requested - write tests FIRST, ensure FAIL before implementation

**Organization**: Tasks grouped by user story with TDD cycle (Red-Green-Refactor) within each phase

---

## Format: `- [ ] [ID] [P?] [Story] Description with file path`

- **[P]**: Task can run in parallel (different files, no dependencies on incomplete tasks)
- **[Story]**: User story label (US1, US2, US3, US4) - REQUIRED for story phase tasks only
- **File paths**: Exact locations for all code changes

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Create project structure and configure tooling

**Expected Duration**: 10 minutes

- [x] T001 Create project structure: calculator.py, tests/ directory at repository root
- [x] T002 Create pyproject.toml with uv configuration, pytest, mypy, black, pytest-cov dependencies
- [x] T003 [P] Create .gitignore with Python-specific entries (venv/, __pycache__/, *.pyc, .pytest_cache/, .mypy_cache/, .coverage, htmlcov/)
- [x] T004 [P] Create empty test files: tests/test_tokenizer.py, tests/test_parser.py, tests/test_evaluator.py, tests/test_cli.py, tests/test_edge_cases.py
- [x] T005 Verify uv environment initializes and dependencies install without errors

**Checkpoint**: Project structure ready, dependencies installed, tests directory prepared

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core components that MUST be complete before user story implementation

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Component 1: Tokenizer (Foundation for all stories)

The Tokenizer converts string input into tokens. All user stories depend on this.

**TDD Cycle for Tokenizer**:

#### RED Phase (Write failing tests first)

- [x] T006 [P] Write tokenizer tests: basic operators (+, -, *, /) in tests/test_tokenizer.py
- [x] T007 [P] Write tokenizer tests: positive integers, whitespace handling in tests/test_tokenizer.py
- [x] T008 [P] Write tokenizer tests: unary minus detection (start of expression, after operators) in tests/test_tokenizer.py
- [x] T009 [P] Write tokenizer tests: invalid characters raise errors in tests/test_tokenizer.py
- [x] T010 [P] Write tokenizer tests: empty/whitespace-only input raises errors in tests/test_tokenizer.py

**Verify these tests FAIL before proceeding to GREEN phase**

#### GREEN Phase (Minimal implementation to pass tests)

- [x] T011 Implement Tokenizer class with tokenize() method in calculator.py
- [x] T012 Implement TokenType enum (NUMBER, PLUS, MINUS, MULTIPLY, DIVIDE, EOF) in calculator.py
- [x] T013 Implement Token dataclass with type and value in calculator.py
- [x] T014 Implement number parsing (positive integers) in calculator.py
- [x] T015 Implement operator tokenization (+, -, *, /) in calculator.py
- [x] T016 Implement unary minus detection (context-sensitive: start, after operators) in calculator.py
- [x] T017 Implement whitespace skipping in calculator.py
- [x] T018 Implement error detection for invalid characters in calculator.py
- [x] T019 Run pytest on tokenizer tests - ALL MUST PASS

#### REFACTOR Phase (Clean up, optimize, document)

- [x] T020 Add type hints to Tokenizer class methods in calculator.py
- [x] T021 Add docstrings explaining tokenization logic in calculator.py
- [x] T022 Run mypy strict mode - MUST have 0 errors in calculator.py

**Checkpoint**: Tokenizer fully implemented and tested, all tokenizer tests pass

---

### Component 2: Parser (Foundation for all stories)

The Parser converts tokens into an Abstract Syntax Tree (AST) respecting BODMAS and unary minus. All user stories depend on this.

**Grammar**:
```
expression := term ((PLUS | MINUS) term)*
term       := factor ((MULTIPLY | DIVIDE) factor)*
factor     := NUMBER | UNARY_MINUS factor
```

**TDD Cycle for Parser**:

#### RED Phase (Write failing tests first)

- [x] T023 [P] Write parser tests: simple addition (5 + 3) in tests/test_parser.py
- [x] T024 [P] Write parser tests: simple subtraction, multiplication, division in tests/test_parser.py
- [x] T025 [P] Write parser tests: BODMAS precedence (2 + 3 * 4 = 14) in tests/test_parser.py
- [x] T026 [P] Write parser tests: left-to-right associativity (10 - 5 - 2 = 3) in tests/test_parser.py
- [x] T027 [P] Write parser tests: unary minus at start and after operators in tests/test_parser.py
- [x] T028 [P] Write parser tests: malformed expressions raise errors in tests/test_parser.py
- [x] T029 [P] Write parser tests: empty token list raises error in tests/test_parser.py

**Verify these tests FAIL before proceeding to GREEN phase**

#### GREEN Phase (Minimal implementation to pass tests)

- [x] T030 Implement ASTNode base class and subclasses (NumberNode, BinaryOpNode, UnaryOpNode) in calculator.py
- [x] T031 Implement Parser class with parse() method in calculator.py
- [x] T032 Implement expression() method (handles PLUS/MINUS, left-to-right) in calculator.py
- [x] T033 Implement term() method (handles MULTIPLY/DIVIDE, left-to-right) in calculator.py
- [x] T034 Implement factor() method (handles NUMBER and UNARY_MINUS) in calculator.py
- [x] T035 Implement error handling for malformed expressions in calculator.py
- [x] T036 Run pytest on parser tests - ALL MUST PASS

#### REFACTOR Phase (Clean up, optimize, document)

- [x] T037 Add type hints to Parser and AST classes in calculator.py
- [x] T038 Add docstrings explaining recursive descent grammar in calculator.py
- [x] T039 Run mypy strict mode - MUST have 0 errors in calculator.py

**Checkpoint**: Parser fully implemented and tested, all parser tests pass, BODMAS precedence verified

---

### Component 3: Evaluator (Foundation for all stories)

The Evaluator walks the AST and computes results, handling integer division truncation toward zero and detecting division by zero. All user stories depend on this.

**TDD Cycle for Evaluator**:

#### RED Phase (Write failing tests first)

- [x] T040 [P] Write evaluator tests: number evaluation in tests/test_evaluator.py
- [x] T041 [P] Write evaluator tests: basic arithmetic (+, -, *, /) in tests/test_evaluator.py
- [x] T042 [P] Write evaluator tests: integer division truncation toward zero (15 / 2 = 7, -7 / 2 = -3) in tests/test_evaluator.py
- [x] T043 [P] Write evaluator tests: division by zero raises DivisionByZeroError in tests/test_evaluator.py
- [x] T044 [P] Write evaluator tests: unary minus evaluation in tests/test_evaluator.py
- [x] T045 [P] Write evaluator tests: complex expressions with operator precedence in tests/test_evaluator.py

**Verify these tests FAIL before proceeding to GREEN phase**

#### GREEN Phase (Minimal implementation to pass tests)

- [x] T046 Implement custom exception hierarchy in calculator.py:
  - CalculatorError (base)
  - DivisionByZeroError
  - InvalidOperandError
  - InvalidOperatorError
  - MalformedExpressionError
- [x] T047 Implement Evaluator class with evaluate() method in calculator.py
- [x] T048 Implement number evaluation (return value) in calculator.py
- [x] T049 Implement binary operation evaluation in calculator.py
- [x] T050 Implement division using int(left / right) for truncation toward zero in calculator.py
- [x] T051 Implement division by zero detection and error raising in calculator.py
- [x] T052 Implement unary minus evaluation in calculator.py
- [x] T053 Run pytest on evaluator tests - ALL MUST PASS

#### REFACTOR Phase (Clean up, optimize, document)

- [x] T054 Add type hints to Evaluator class in calculator.py
- [x] T055 Add docstrings for evaluation logic in calculator.py
- [x] T056 Run mypy strict mode - MUST have 0 errors in calculator.py

**Checkpoint**: Evaluator fully implemented and tested, integer division truncation verified, all evaluator tests pass

---

### Component 4: Exception Mapping and Error Messages (Foundation for all stories)

Create error message mapping for CLI output. All user stories depend on this for error handling.

**TDD Cycle for Exception Mapping**:

#### RED Phase (Write failing tests first)

- [x] T057 [P] Write tests for error message formatting in tests/test_cli.py (DivisionByZeroError → "Error: Division by zero is not allowed")
- [x] T058 [P] Write tests for error message formatting (MalformedExpressionError → "Error: Malformed expression")
- [x] T059 [P] Write tests for error message formatting (InvalidOperandError → "Error: Invalid operand")

**Verify these tests FAIL before proceeding to GREEN phase**

#### GREEN Phase (Minimal implementation to pass tests)

- [x] T060 Create ERROR_MESSAGES dictionary mapping exception types to user-friendly messages in calculator.py
- [x] T061 Implement error message lookup function in calculator.py
- [x] T062 Run pytest on error message tests - ALL MUST PASS

#### REFACTOR Phase

- [x] T063 Add type hints to error handling functions in calculator.py
- [x] T064 Run mypy strict mode - MUST have 0 errors in calculator.py

**Checkpoint**: Exception mapping complete, error messages verified, foundation ready for user stories

---

## Phase 3: User Story 1 - Basic Arithmetic Calculation (Priority: P1) 🎯 MVP

**Goal**: Calculate simple expressions with +, -, *, / and return integer results

**Independent Test**: Run calculator with "5 + 3", "10 - 4", "6 * 7", "20 / 4" and verify correct integer results

**Acceptance Scenarios**:
- `calculator "5 + 3"` → outputs `8` to stdout, exit 0
- `calculator "10 - 4"` → outputs `6` to stdout, exit 0
- `calculator "6 * 7"` → outputs `42` to stdout, exit 0
- `calculator "20 / 4"` → outputs `5` to stdout, exit 0
- `calculator "15 / 2"` → outputs `7` to stdout (integer division), exit 0
- `calculator "10 - 5 - 2"` → outputs `3` to stdout (left-to-right), exit 0
- `calculator "20 - 10 - 5 - 3"` → outputs `2` to stdout (chained), exit 0

### TDD Cycle for User Story 1

#### RED Phase (Write failing tests first)

- [x] T065 [P] [US1] Write CLI integration tests for basic arithmetic in tests/test_cli.py:
  - Test: "5 + 3" outputs "8" to stdout, exit 0
  - Test: "10 - 4" outputs "6" to stdout, exit 0
  - Test: "6 * 7" outputs "42" to stdout, exit 0
  - Test: "20 / 4" outputs "5" to stdout, exit 0
- [x] T066 [P] [US1] Write CLI integration tests for integer division in tests/test_cli.py:
  - Test: "15 / 2" outputs "7" to stdout, exit 0
- [x] T067 [P] [US1] Write CLI integration tests for chained operations in tests/test_cli.py:
  - Test: "10 - 5 - 2" outputs "3" to stdout, exit 0
  - Test: "20 - 10 - 5 - 3" outputs "2" to stdout, exit 0

**Verify these tests FAIL before proceeding to GREEN phase**

#### GREEN Phase (Minimal implementation to pass tests)

- [x] T068 [US1] Implement main() function in calculator.py:
  - Check sys.argv for expression
  - Call tokenize → parse → evaluate pipeline
  - Print result to stdout on success, exit 0
  - Catch exceptions, print to stderr, exit 1
- [x] T069 [US1] Implement command-line argument handling in main() function
- [x] T070 [US1] Implement stdout output for successful results in main() function
- [x] T071 [US1] Implement exit code handling (0 for success, 1 for errors) in main() function
- [x] T072 [US1] Add if __name__ == "__main__": main() at end of calculator.py
- [x] T073 [US1] Run pytest on US1 CLI tests - ALL MUST PASS
- [x] T074 [US1] Test manually: `python calculator.py "5 + 3"` outputs `8`, exit 0

#### REFACTOR Phase (Clean up, optimize, document)

- [x] T075 [US1] Add type hints to main() function in calculator.py
- [x] T076 [US1] Add docstring to main() function explaining CLI contract in calculator.py
- [x] T077 [US1] Run mypy strict mode - MUST have 0 errors in calculator.py
- [x] T078 [US1] Run black formatter on calculator.py - MUST have 0 differences

**Checkpoint**: User Story 1 fully functional. Test independently: `python calculator.py "5 + 3"` works correctly. STOP and validate before proceeding.

---

## Phase 4: User Story 2 - BODMAS Operator Precedence (Priority: P2)

**Goal**: Ensure complex expressions with mixed operators apply correct precedence (multiplication/division before addition/subtraction)

**Independent Test**: Run expressions with multiple operators and verify precedence:
- `calculator "2 + 3 * 4"` → 14 (not 20)
- `calculator "10 - 6 / 2"` → 7 (not 2)
- `calculator "100 / 10 / 2"` → 5 (left-to-right)

**Acceptance Scenarios**:
- `calculator "2 + 3 * 4"` → outputs `14` to stdout, exit 0 (multiplication before addition)
- `calculator "10 - 6 / 2"` → outputs `7` to stdout, exit 0 (division before subtraction)
- `calculator "2 * 3 + 4 * 5"` → outputs `26` to stdout, exit 0
- `calculator "100 / 10 / 2"` → outputs `5` to stdout, exit 0 (left-to-right)
- `calculator "20 / 4 / 2"` → outputs `2` to stdout, exit 0 (chained division)
- `calculator "10 - 3 - 2"` → outputs `5` to stdout, exit 0 (subtraction left-to-right, NOT 9)

### TDD Cycle for User Story 2

#### RED Phase (Write failing tests first)

- [x] T079 [P] [US2] Write CLI integration tests for BODMAS precedence in tests/test_edge_cases.py:
  - Test: "2 + 3 * 4" outputs "14" to stdout, exit 0
  - Test: "10 - 6 / 2" outputs "7" to stdout, exit 0
  - Test: "2 * 3 + 4 * 5" outputs "26" to stdout, exit 0
- [x] T080 [P] [US2] Write CLI tests for chained operations in tests/test_edge_cases.py:
  - Test: "100 / 10 / 2" outputs "5" to stdout, exit 0
  - Test: "20 / 4 / 2" outputs "2" to stdout, exit 0
  - Test: "10 - 3 - 2" outputs "5" to stdout, exit 0

**Verify these tests FAIL before proceeding to GREEN phase**

**Note**: These tests should ALREADY PASS because Parser and Evaluator handle BODMAS correctly. If any FAIL, go back to Phase 2 and debug parser/evaluator.

#### GREEN Phase (Verify correct behavior)

- [x] T081 [US2] Run all US2 CLI tests - ALL MUST PASS (no new code needed, parser already handles this)
- [x] T082 [US2] Test manually:
  - `python calculator.py "2 + 3 * 4"` outputs `14`
  - `python calculator.py "10 - 6 / 2"` outputs `7`
  - `python calculator.py "100 / 10 / 2"` outputs `5`

#### REFACTOR Phase

- [x] T083 [US2] Run full test suite: `pytest --cov=calculator --cov-report=term-missing`
- [x] T084 [US2] Verify coverage is 80%+ (constitution requirement)
- [x] T085 [US2] Run mypy strict mode - MUST have 0 errors
- [x] T086 [US2] Run black formatter - MUST have 0 differences

**Checkpoint**: User Story 2 verified. BODMAS precedence works correctly. Parser handles all precedence cases. Stop and validate before proceeding.

---

## Phase 5: User Story 3 - Division by Zero Handling (Priority: P3)

**Goal**: Detect division by zero and display clear error message to stderr with exit code 1

**Independent Test**: Run expressions dividing by zero and verify error handling:
- `calculator "10 / 0"` → error message to stderr, exit 1
- `calculator "5 + 10 / 0"` → error message to stderr, exit 1

**Acceptance Scenarios**:
- `calculator "10 / 0"` → displays "Error: Division by zero is not allowed" to stderr, exit 1
- `calculator "5 + 10 / 0"` → displays error message to stderr (detected during evaluation), exit 1

### TDD Cycle for User Story 3

#### RED Phase (Write failing tests first)

- [x] T087 [P] [US3] Write CLI tests for division by zero in tests/test_edge_cases.py:
  - Test: "10 / 0" outputs error message to stderr, exit 1
  - Test: "5 + 10 / 0" outputs error message to stderr, exit 1
- [x] T088 [P] [US3] Write tests verifying error message format in tests/test_edge_cases.py:
  - Test: stderr output starts with "Error:"
  - Test: exit code is 1 (not 0)

**Verify these tests FAIL before proceeding to GREEN phase**

#### GREEN Phase (Minimal implementation to pass tests)

- [x] T089 [US3] Implement stderr output for errors in main() function in calculator.py
- [x] T090 [US3] Map DivisionByZeroError to user-friendly message in ERROR_MESSAGES in calculator.py
- [x] T091 [US3] Verify error message printed to stderr (not stdout) in main() function
- [x] T092 [US3] Run pytest on US3 tests - ALL MUST PASS
- [x] T093 [US3] Test manually: `python calculator.py "10 / 0"` outputs error to stderr, exit 1

#### REFACTOR Phase

- [x] T094 [US3] Run full test suite: `pytest tests/`
- [x] T095 [US3] Run mypy strict mode - MUST have 0 errors
- [x] T096 [US3] Run black formatter - MUST have 0 differences

**Checkpoint**: User Story 3 fully functional. Division by zero error handling verified. Stop and validate before proceeding.

---

## Phase 6: User Story 4 - Invalid Input Handling (Priority: P4)

**Goal**: Detect and reject invalid input (non-integers, malformed expressions, unsupported characters) with clear error messages

**Independent Test**: Run expressions with invalid input and verify error handling:
- `calculator "5 + abc"` → error message to stderr, exit 1
- `calculator ""` → error message to stderr, exit 1
- `calculator "   "` → error message to stderr, exit 1
- `calculator "5 ++"` → error message to stderr, exit 1
- `calculator "5 @ 3"` → error message to stderr, exit 1

**Acceptance Scenarios**:
- `calculator "5 + abc"` → displays error message to stderr, exit 1
- `calculator ""` → displays error message about empty input to stderr, exit 1
- `calculator "   "` → displays error message about empty/whitespace input to stderr, exit 1
- `calculator "5 ++"` → displays error message about malformed expression to stderr, exit 1
- `calculator "5 @ 3"` → displays error message about invalid operator to stderr, exit 1

### TDD Cycle for User Story 4

#### RED Phase (Write failing tests first)

- [x] T097 [P] [US4] Write CLI tests for invalid operands in tests/test_edge_cases.py:
  - Test: "5 + abc" outputs error to stderr, exit 1
  - Test: "5 + 3.5" outputs error to stderr (non-integers), exit 1
- [x] T098 [P] [US4] Write CLI tests for empty/whitespace input in tests/test_edge_cases.py:
  - Test: "" outputs error to stderr, exit 1
  - Test: "   " outputs error to stderr, exit 1
  - Test: no argument provided outputs error to stderr, exit 1
- [x] T099 [P] [US4] Write CLI tests for malformed expressions in tests/test_edge_cases.py:
  - Test: "5 ++" outputs error to stderr, exit 1
  - Test: "5 +" outputs error to stderr, exit 1
  - Test: "+ 5" outputs error to stderr, exit 1
- [x] T100 [P] [US4] Write CLI tests for invalid operators in tests/test_edge_cases.py:
  - Test: "5 @ 3" outputs error to stderr, exit 1
  - Test: "5 # 3" outputs error to stderr, exit 1

**Verify these tests FAIL before proceeding to GREEN phase**

#### GREEN Phase (Minimal implementation to pass tests)

- [x] T101 [US4] Implement empty/whitespace input check in main() function in calculator.py
- [x] T102 [US4] Implement error message for empty input in ERROR_MESSAGES in calculator.py
- [x] T103 [US4] Verify InvalidOperandError caught and mapped to error message in main() function
- [x] T104 [US4] Verify InvalidOperatorError caught and mapped to error message in main() function
- [x] T105 [US4] Verify MalformedExpressionError caught and mapped to error message in main() function
- [x] T106 [US4] Run pytest on US4 tests - ALL MUST PASS
- [x] T107 [US4] Test manually:
  - `python calculator.py ""` outputs error to stderr
  - `python calculator.py "5 + abc"` outputs error to stderr
  - `python calculator.py "5 ++"` outputs error to stderr

#### REFACTOR Phase

- [x] T108 [US4] Run full test suite: `pytest --cov=calculator --cov-report=term-missing`
- [x] T109 [US4] Verify coverage is 80%+ (constitution requirement)
- [x] T110 [US4] Run mypy strict mode - MUST have 0 errors
- [x] T111 [US4] Run black formatter - MUST have 0 differences

**Checkpoint**: User Story 4 fully functional. Invalid input error handling verified. All user stories complete and independently testable.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final validation, code quality, and documentation

- [ ] T112 [P] Run complete test suite: `pytest tests/ -v` (all tests MUST PASS)
- [ ] T113 [P] Run coverage report: `pytest --cov=calculator --cov-report=term-missing` (MUST be 80%+)
- [ ] T114 [P] Run mypy strict: `mypy calculator.py --strict` (MUST have 0 errors)
- [ ] T115 [P] Run black formatter: `black calculator.py tests/` (MUST have 0 differences)
- [ ] T116 Validate all acceptance scenarios from spec.md:
  - US1: Basic arithmetic (7 scenarios)
  - US2: BODMAS precedence (6 scenarios)
  - US3: Division by zero (2 scenarios)
  - US4: Invalid input (5+ scenarios)
- [ ] T117 Test CLI with sample inputs:
  - `python calculator.py "2 + 3"` → 5
  - `python calculator.py "2 + 3 * 4"` → 14
  - `python calculator.py "10 / 0"` → error
  - `python calculator.py ""` → error
- [ ] T118 Verify exit codes: success (0), error (1)
- [ ] T119 Verify stdout/stderr separation: results to stdout, errors to stderr
- [ ] T120 Final code review: Check all type hints, docstrings, error handling
- [ ] T121 Create README.md with usage examples and test instructions

**Final Checkpoint**: All tests pass, coverage 80%+, mypy 0 errors, black formatted. Calculator ready for deployment.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies - can start immediately
- **Phase 2 (Foundational)**: Depends on Phase 1 completion - BLOCKS all user stories
  - Tokenizer MUST be complete before Parser
  - Parser MUST be complete before Evaluator
  - Evaluator MUST be complete before CLI
  - Exception mapping MUST be complete before CLI
- **Phases 3-6 (User Stories)**: All depend on Phase 2 completion
  - US1 can start immediately after Phase 2
  - US2, US3, US4 can start immediately after Phase 2 (independent of US1)
- **Phase 7 (Polish)**: Depends on all user stories completion

### Critical Path

1. Phase 1: Setup (T001-T005)
2. Phase 2: Tokenizer (T006-T022)
3. Phase 2: Parser (T023-T039)
4. Phase 2: Evaluator (T040-T056)
5. Phase 2: Exception Mapping (T057-T064)
6. Phase 3: US1 CLI (T065-T078) ← **MVP stops here**
7. Phase 4: US2 Precedence (T079-T086)
8. Phase 5: US3 Div by Zero (T087-T096)
9. Phase 6: US4 Input Validation (T097-T111)
10. Phase 7: Polish (T112-T121)

### Parallel Opportunities

**Within Phase 1**: T003, T004 can run in parallel (different files)

**Within Phase 2 Tokenizer (RED)**: T006-T010 can run in parallel (tests only)

**Within Phase 2 Tokenizer (GREEN)**: T011-T018 must run sequentially (same file, building on each other)

**Within Phase 2 Parser (RED)**: T023-T029 can run in parallel (tests only)

**Within Phase 2 Parser (GREEN)**: T030-T036 must run sequentially (same file, building on each other)

**Within Phase 2 Evaluator (RED)**: T040-T045 can run in parallel (tests only)

**Within Phase 2 Evaluator (GREEN)**: T046-T053 must run sequentially (same file, building on each other)

**Within US1 (RED)**: T065-T067 can run in parallel (tests only)

**Within US2 (RED)**: T079-T080 can run in parallel (tests only)

**Within US3 (RED)**: T087-T088 can run in parallel (tests only)

**Within US4 (RED)**: T097-T100 can run in parallel (tests only)

**Phase 7 Polish**: T112-T115 can run in parallel (different commands)

**User Stories can start in parallel ONLY AFTER Phase 2 is complete:**
- Developer A: US1 (T065-T078)
- Developer B: US2 (T079-T086) *after Phase 2 complete*
- Developer C: US3 (T087-T096) *after Phase 2 complete*
- Developer D: US4 (T097-T111) *after Phase 2 complete*

---

## Implementation Strategy

### MVP First (Recommended)

1. **Complete Phase 1**: Setup (5 minutes)
2. **Complete Phase 2**: Foundational (2-3 hours)
   - Tokenizer: ~30 min RED + 30 min GREEN + 15 min REFACTOR
   - Parser: ~45 min RED + 1 hour GREEN + 15 min REFACTOR
   - Evaluator: ~30 min RED + 45 min GREEN + 15 min REFACTOR
   - Exception Mapping: ~15 min RED + 15 min GREEN + 10 min REFACTOR
3. **Complete Phase 3**: User Story 1 (20 minutes)
   - Write tests: 10 min
   - Implement CLI: 5 min
   - Refactor & verify: 5 min
4. **STOP and VALIDATE**: Test US1 independently
   - Run `python calculator.py "5 + 3"` → verify 8, exit 0
   - Run all US1 acceptance scenarios
5. **Deploy/demo MVP if ready**

### Incremental Delivery

After MVP:

1. Add US2 (20 minutes) → Verify BODMAS works → Deploy/Demo
2. Add US3 (20 minutes) → Verify error handling → Deploy/Demo
3. Add US4 (20 minutes) → Verify input validation → Deploy/Demo
4. Polish & cleanup (15 minutes) → Final validation → Deploy

---

## Task Checklist Notes

- Each task MUST be independently completable
- Verify tests FAIL before implementing (RED-GREEN-REFACTOR cycle)
- Run pytest and mypy frequently during GREEN phase
- Commit after completing each component
- Stop at Phase 3 checkpoint to validate MVP independently
- Avoid skipping the REFACTOR phase (type hints, docstrings, formatting required)

---

## Success Criteria Validation Checklist

After completing all phases, verify against spec.md:

- [ ] SC-001: All four operations work (+-*/)
- [ ] SC-002: BODMAS precedence correct (mult/div before add/sub)
- [ ] SC-003: Division by zero handled with error message
- [ ] SC-004: Invalid input handled with error message
- [ ] SC-005: Immediate execution (no delays)
- [ ] SC-006: Clear error messages
- [ ] SC-007: Whitespace flexibility (leading/trailing/between operators)
- [ ] SC-008: Exit codes correct (0 success, 1 error)

All acceptance scenarios from all 4 user stories verified? → **READY FOR PRODUCTION**
