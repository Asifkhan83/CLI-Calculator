# Data Model: Modulo Operator

**Feature**: 002-modulo-operator
**Date**: 2026-01-06

## Overview

This feature extends existing data structures rather than creating new ones. The modulo operator integrates into the existing token and AST (Abstract Syntax Tree) model.

## Entity Changes

### 1. Token (Extended)

**Current State**: Tokens are strings representing numbers and operators.

**Change**: Add `%` as a valid operator token.

| Token Type | Examples | Notes |
|------------|----------|-------|
| NUMBER | "123", "0", "42" | Unchanged |
| OPERATOR | "+", "-", "*", "/", "%" | Added "%" |
| GROUPING | "(", ")" | Unchanged |

### 2. Exception Hierarchy (Extended)

**Current Hierarchy**:
```
CalculatorError (base)
├── DivisionByZeroError
└── InvalidInputError
```

**New Hierarchy**:
```
CalculatorError (base)
├── DivisionByZeroError
├── ModuloByZeroError    # NEW
└── InvalidInputError
```

**New Class Definition**:
```python
class ModuloByZeroError(CalculatorError):
    """Raised when attempting modulo by zero."""
    pass
```

## Operator Precedence Model

| Level | Operators | Associativity | Parser Method |
|-------|-----------|---------------|---------------|
| 1 (lowest) | +, - | Left-to-right | _parse_expression() |
| 2 (higher) | *, /, % | Left-to-right | _parse_term() |
| 3 (highest) | unary +/- | Right-to-left | _parse_factor() |

**Note**: `%` shares precedence level 2 with `*` and `/`.

## State Transitions

N/A - The calculator is stateless. Each expression is evaluated independently.

## Validation Rules

| Rule | Description | Error |
|------|-------------|-------|
| Modulo by zero | Right operand of % cannot be 0 | ModuloByZeroError |
| Valid token | % must be recognized as operator | InvalidInputError |
| Integer operands | Both operands must be integers | InvalidInputError |

## Data Flow

```
Input String
    ↓
Tokenizer (recognizes %)
    ↓
Token List [..., "%", ...]
    ↓
Parser._parse_term() (handles %)
    ↓
Integer Result (a % b)
```
