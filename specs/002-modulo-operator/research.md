# Research: Modulo Operator

**Feature**: 002-modulo-operator
**Date**: 2026-01-06

## Research Summary

This document captures research findings for implementing the modulo operator in the CLI Calculator.

## Decision 1: Modulo Semantics for Negative Numbers

**Decision**: Use Python's native modulo semantics (floored division)

**Rationale**: 
- Python's `%` operator already implements floored division semantics
- Result has the same sign as the divisor
- Consistent with existing Python behavior users expect
- No additional implementation complexity

**Alternatives Considered**:
1. Truncated division (C-style): Rejected - would require custom implementation
2. Always positive result: Rejected - non-standard, confusing

**Examples**:
- `-10 % 3 = 2` (Python floored)
- `10 % -3 = -2` (Python floored)
- `-10 % -3 = -1` (Python floored)

## Decision 2: Error Handling Approach

**Decision**: Create separate `ModuloByZeroError` exception class

**Rationale**:
- Clear distinction between division and modulo errors
- Better error messages for users
- Consistent with existing `DivisionByZeroError` pattern
- Easy to catch and handle separately if needed

**Alternatives Considered**:
1. Reuse `DivisionByZeroError`: Rejected - less specific error messages
2. Generic `ArithmeticError`: Rejected - doesn't follow project conventions

## Decision 3: Parser Integration Point

**Decision**: Add `%` handling in `_parse_term()` method

**Rationale**:
- Same precedence as `*` and `/` (BODMAS)
- Left-to-right associativity maintained
- Minimal code changes (single method modification)
- Clean integration with existing recursive descent parser

**Alternatives Considered**:
1. Separate precedence level: Rejected - not mathematically correct
2. New parser method: Rejected - unnecessary complexity

## Decision 4: Tokenizer Pattern Update

**Decision**: Add `%` to existing TOKEN_PATTERN regex character class

**Rationale**:
- Single character addition to regex
- Maintains existing tokenization behavior
- No new token types needed (string-based)

**Pattern Change**:
```python
# Before
TOKEN_PATTERN = re.compile(r'\s*(\d+|[+\-*/()])\s*')

# After
TOKEN_PATTERN = re.compile(r'\s*(\d+|[+\-*/%()])\s*')
```

## Open Questions Resolved

All technical questions have been resolved. No remaining NEEDS CLARIFICATION items.

## References

- Python `%` operator documentation
- Existing calculator.py implementation (calculator.py:22-103)
- Project constitution (integer arithmetic, single-file constraint)
