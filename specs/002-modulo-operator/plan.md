# Implementation Plan: Modulo Operator

**Branch**: `002-modulo-operator` | **Date**: 2026-01-06 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-modulo-operator/spec.md`

## Summary

Add the modulo (%) operator to the CLI Calculator to compute integer remainders. The operator will have the same precedence as multiplication and division (BODMAS), evaluate left-to-right with same-precedence operators, and handle modulo-by-zero errors gracefully. Implementation extends the existing Tokenizer and Parser classes with minimal changes.

## Technical Context

**Language/Version**: Python 3.12 (latest stable)
**Primary Dependencies**: None (standard library only - re, sys, typing)
**Storage**: N/A (stateless calculator)
**Testing**: pytest with pytest-cov for coverage
**Target Platform**: CLI (Windows, Linux, macOS)
**Project Type**: Single-file CLI application
**Performance Goals**: Instant response (<100ms for any expression)
**Constraints**: Single-file implementation (calculator.py), integer-only arithmetic
**Scale/Scope**: Simple CLI tool, no concurrency requirements

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Python-Only CLI | PASS | Single-file calculator.py, CLI-only |
| II. Code Quality (PEP 8) | PASS | Will use black formatter |
| III. Type Safety | PASS | Type hints on all functions |
| IV. Integer Arithmetic | PASS | Modulo returns integers |
| V. Error Handling | PASS | ModuloByZeroError planned |
| VI. Test-First (TDD) | PASS | Tests written before implementation |
| VII. Minimal Dependencies | PASS | Standard library only |
| VIII. Feature Development | PASS | Sequential development with commits |

**Gate Result**: PASS - All constitution principles satisfied.

## Project Structure

### Documentation (this feature)

```text
specs/002-modulo-operator/
├── spec.md              # Feature specification (created)
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── checklists/          # Quality checklists
│   └── requirements.md  # Spec quality checklist (created)
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
calculator.py            # Single-file implementation (modify)
tests/
└── test_modulo.py       # New modulo-specific tests (create)
```

**Structure Decision**: Single-file implementation per constitution. All code changes in `calculator.py`. New test file `test_modulo.py` for modulo-specific tests to maintain separation of concerns.

## Complexity Tracking

> No violations - implementation follows constitution principles.

| Aspect | Assessment |
|--------|------------|
| Code Changes | Minimal - ~20 lines added to calculator.py |
| New Classes | None - extends existing Tokenizer/Parser |
| New Dependencies | None |
| Architecture Impact | None - additive change only |

## Implementation Approach

### Changes Required

#### 1. Tokenizer Class (calculator.py:22-57)

**Current**: `TOKEN_PATTERN = re.compile(r'\s*(\d+|[+\-*/()])\s*')`

**Change**: Add `%` to the character class:
```python
TOKEN_PATTERN = re.compile(r'\s*(\d+|[+\-*/%()])\s*')
```

**Impact**: Single character addition to regex pattern.

#### 2. Parser._parse_term() Method (calculator.py:89-103)

**Current**: Handles `*` and `/` operators

**Change**: Add `%` to the same precedence level:
```python
while self.tokenizer.peek() in ('*', '/', '%'):
    operator = self.tokenizer.consume()
    right = self._parse_factor()
    if operator == '*':
        left = left * right
    elif operator == '/':
        if right == 0:
            raise DivisionByZeroError("Division by zero is not allowed")
        left = left // right
    else:  # operator == '%'
        if right == 0:
            raise ModuloByZeroError("Modulo by zero is not allowed")
        left = left % right
```

**Impact**: ~8 lines added to existing method.

#### 3. New Exception Class (calculator.py:12-19)

**Add**: `ModuloByZeroError` class

```python
class ModuloByZeroError(CalculatorError):
    """Raised when attempting modulo by zero."""
    pass
```

**Decision**: Create separate `ModuloByZeroError` for clarity in error messages.

#### 4. Main Function Update (calculator.py:150-180)

**Change**: Add exception handler for `ModuloByZeroError`:
```python
except ModuloByZeroError as e:
    print(f"Error: {e}")
```

### Test Strategy (TDD)

#### RED Phase - Write Failing Tests First

1. **test_modulo.py** - New test file:
   - `test_basic_modulo()` - 10 % 3 = 1, 15 % 5 = 0, etc.
   - `test_modulo_precedence()` - 10 + 7 % 3 = 11, etc.
   - `test_modulo_left_to_right()` - 2 * 10 % 3 = 2, etc.
   - `test_modulo_by_zero()` - raises ModuloByZeroError
   - `test_modulo_with_negatives()` - -10 % 3, 10 % -3, etc.
   - `test_modulo_edge_cases()` - 3 % 10, 10 % 1, etc.

2. **test_calculator.py** - Verify no regression in existing functionality

#### GREEN Phase - Minimal Implementation

Implement changes in order:
1. Add ModuloByZeroError class
2. Update TOKEN_PATTERN regex
3. Update _parse_term() method
4. Update main() exception handling

#### REFACTOR Phase

1. Run black formatter
2. Run mypy strict mode
3. Verify 80%+ coverage
4. Review for code quality

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Regex pattern break | Low | High | Test all existing operations first |
| Precedence incorrect | Low | Medium | Explicit tests for BODMAS |
| Negative modulo edge cases | Medium | Low | Follow Python semantics, document |
| Breaking existing tests | Low | High | Run full test suite before/after |

## Definition of Done

- [ ] All new tests pass (test_modulo.py)
- [ ] All existing tests pass (no regression)
- [ ] Coverage >= 80%
- [ ] mypy strict mode: 0 errors
- [ ] black formatter: 0 differences
- [ ] All acceptance scenarios from spec verified
- [ ] Code committed and pushed to branch
- [ ] PR created with constitution compliance checklist
