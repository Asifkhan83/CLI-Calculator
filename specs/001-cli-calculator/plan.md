# Implementation Plan: CLI Calculator

**Branch**: `001-cli-calculator` | **Date**: 2026-01-05 | **Spec**: [specs/001-cli-calculator/spec.md](../spec.md)
**Input**: Feature specification from `/specs/001-cli-calculator/spec.md`

## Summary

Single-file Python CLI calculator with integer arithmetic, BODMAS precedence, and comprehensive error handling. Uses recursive descent parser for expression evaluation with context-sensitive tokenization to handle unary minus, left-to-right associativity for equal precedence, and integer division truncating toward zero per specification.

## Technical Context

**Language/Version**: Python 3.11+ (constitution mandates latest stable)
**Primary Dependencies**: pytest, pytest-cov, mypy, black (all development/testing)
**Storage**: N/A (stateless CLI)
**Testing**: pytest with pytest-cov for coverage reporting
**Target Platform**: Cross-platform CLI (Linux, macOS, Windows)
**Project Type**: Single file CLI application
**Performance Goals**: Immediate execution (no perceptible delay per SC-005)
**Constraints**: Integer arithmetic only, BODMAS precedence, division truncation toward zero
**Scale/Scope**: Single calculator.py file, 5 test modules, ~500-800 lines total code

## Constitution Check

✅ **PASS** - All 8 principles satisfied:
1. Python-Only CLI ✓
2. Code Quality (type hints, PEP 8) ✓
3. Type Safety (mypy strict) ✓
4. Test-First (TDD approach) ✓
5. Simplicity & Minimal Dependencies ✓
6. Feature Development Strategy (single file, clear separation of concerns) ✓
7. ADR Process (architectural decisions documented in plan) ✓
8. CI/CD Guardrails (pytest 80%+, mypy 0 errors, black format) ✓

## Project Structure

### Documentation (this feature)

```text
specs/001-cli-calculator/
├── plan.md              # This file (approved implementation plan)
├── spec.md              # Feature specification (262 lines, fully clarified)
├── checklists/
│   └── requirements.md  # Specification validation checklist
└── (contracts/, research.md, data-model.md not needed for simple CLI)
```

### Source Code (repository root)

```text
calculator.py           # Single-file implementation (main deliverable)
tests/
├── test_tokenizer.py   # Tokenization component tests
├── test_parser.py      # Parser component tests
├── test_evaluator.py   # Evaluator component tests
├── test_cli.py         # CLI integration tests
└── test_edge_cases.py  # Edge case tests (division, unary minus, chains)
pyproject.toml          # uv project config with dependencies
.gitignore              # Python-specific ignores
```

**Structure Decision**: Single file (calculator.py) per constitution mandate, organized into 7 logical sections (types, tokens, exceptions, tokenizer, parser, evaluator, CLI). Test files separated in tests/ directory for modularity and independent testing of each component.

## Complexity Tracking

No complexity violations - architecture is intentionally simple:
- Single file enforces modularity through clear class/function boundaries
- Recursive descent parser is straightforward for simple expression grammar
- No external dependencies beyond standard library
- TDD approach ensures testability from start

---

## Architecture Decisions

### 1. Expression Parsing Approach
**Decision:** Use **Recursive Descent Parser** with separate tokenization phase

**Rationale:**
- Naturally handles operator precedence through grammar rules
- Easier to extend if parentheses are added later
- Clear separation: Tokenizer → Parser → Evaluator
- No external dependencies needed (vs libraries like pyparsing)
- Type-safe and testable

**Alternative Considered:** Shunting Yard Algorithm
- Rejected: More complex for our simple use case
- Would require stack management and postfix conversion
- Less intuitive for maintainability

### 2. Integer Division Strategy
**Python Choice:** Use `int()` function on division result
- Python's `//` operator does floor division (toward negative infinity)
- Spec requires truncation toward zero
- Solution: `int(a / b)` truncates toward zero correctly
- Example: `int(-7 / 2)` = `-3` (correct), `-7 // 2` = `-4` (wrong)

### 3. Error Handling Pattern
**Approach:** Custom exception hierarchy with specific error messages
```python
class CalculatorError(Exception): pass
class DivisionByZeroError(CalculatorError): pass
class InvalidOperandError(CalculatorError): pass
class InvalidOperatorError(CalculatorError): pass
class MalformedExpressionError(CalculatorError): pass
```
- Map exceptions to user-friendly messages at CLI level
- All errors exit with code 1

---

## Implementation Components

### Component 1: Tokenizer
**Purpose:** Convert string input to tokens
```python
Input:  "5 + 3 * -2"
Output: [NUMBER(5), PLUS, NUMBER(3), MULTIPLY, NUMBER(-2)]
```

**Key Features:**
- Handle unary minus (context-sensitive)
- Skip whitespace
- Detect invalid characters
- Support negative integers

### Component 2: Parser (Recursive Descent)
**Grammar (EBNF-like):**
```
expression := term ((PLUS | MINUS) term)*
term       := factor ((MULTIPLY | DIVIDE) factor)*
factor     := NUMBER | UNARY_MINUS factor
```

**Key Features:**
- Left-to-right associativity (natural from left recursion removal)
- BODMAS precedence (multiplication/division before addition/subtraction)
- Unary minus handling in factor

### Component 3: Evaluator
**Purpose:** Walk AST and compute result
```python
- Number nodes → return value
- Binary op nodes → evaluate left, evaluate right, apply operator
- Unary minus nodes → evaluate child, negate
```

**Critical:** Division uses `int(left / right)` for truncation toward zero

### Component 4: CLI Interface
**main() function:**
1. Check sys.argv for expression
2. Handle empty/whitespace input
3. Try: tokenize → parse → evaluate
4. Catch exceptions → map to error messages
5. Print result to stdout (exit 0) OR error to stderr (exit 1)

---

## Test Strategy (TDD Approach)

### Test Order (Red-Green-Refactor)
1. **Tokenizer Tests** (test_tokenizer.py)
   - Basic tokens: numbers, operators
   - Unary minus detection
   - Whitespace handling
   - Invalid character detection

2. **Parser Tests** (test_parser.py)
   - Simple expressions: `5 + 3`
   - Precedence: `2 + 3 * 4` = 14
   - Associativity: `10 - 5 - 2` = 3
   - Unary minus: `-5 + 3` = -2
   - Malformed expression detection

3. **Evaluator Tests** (test_evaluator.py)
   - Basic arithmetic
   - Integer division truncation: `-7 / 2` = -3
   - Division by zero detection
   - Unary minus evaluation

4. **CLI Tests** (test_cli.py)
   - Argument parsing
   - Exit codes (0 for success, 1 for errors)
   - stdout vs stderr separation
   - Empty/whitespace input handling

5. **Edge Case Tests** (test_edge_cases.py)
   - Negative operand combinations
   - Chained operations
   - All error types with specific messages

### Coverage Goal
- Minimum 80% coverage (constitution requirement)
- Target: 95%+ given comprehensive spec

---

## Development Steps

### Phase 1: Project Setup
```bash
# Initialize uv project
uv init --lib
uv add pytest pytest-cov mypy black --dev

# Create directory structure
mkdir tests
touch calculator.py
touch tests/{test_tokenizer,test_parser,test_evaluator,test_cli,test_edge_cases}.py
```

### Phase 2: TDD Cycle (Per Component)
For each component (Tokenizer → Parser → Evaluator → CLI):
1. Write failing tests (RED)
2. Implement minimal code to pass (GREEN)
3. Refactor for clarity (REFACTOR)
4. Run mypy and black before commit

### Phase 3: Integration & Verification
1. Run full test suite: `pytest --cov=calculator --cov-report=term-missing`
2. Type check: `mypy calculator.py --strict`
3. Format: `black calculator.py tests/`
4. Verify all acceptance scenarios from spec.md

---

## Key Implementation Details

### Unary Minus Handling
- **Context-sensitive tokenization:**
  - After `(` or at start → unary
  - After operator → unary
  - After number → binary
- **Parser treatment:** Unary minus as prefix operator in factor rule

### Division Truncation
```python
def divide(self, left: int, right: int) -> int:
    if right == 0:
        raise DivisionByZeroError("Division by zero is not allowed")
    return int(left / right)  # Truncates toward zero
```

### Error Message Mapping
```python
ERROR_MESSAGES = {
    DivisionByZeroError: "Error: Division by zero is not allowed",
    InvalidOperandError: "Error: Invalid operand '{token}'. Only integers are allowed.",
    # ... etc
}
```

---

## Success Criteria Validation

After implementation, verify against spec.md:
- ✓ SC-001: All four operations work
- ✓ SC-002: BODMAS precedence correct
- ✓ SC-003: Division by zero handled
- ✓ SC-004: Invalid input handled
- ✓ SC-005: Immediate execution (no delays)
- ✓ SC-006: Clear error messages
- ✓ SC-007: Whitespace flexibility
- ✓ SC-008: Exit codes correct

---

## Constitution Compliance Checklist

- ✓ Single file (calculator.py)
- ✓ Python with type hints
- ✓ PEP 8 via black
- ✓ pytest with 80%+ coverage
- ✓ mypy strict mode
- ✓ uv package manager
- ✓ Minimal dependencies (standard library only)
- ✓ TDD approach (tests first)

---

## Next Steps

1. Run `/sp.tasks` to generate detailed actionable task list
2. Create project structure files (pyproject.toml, .gitignore, test files)
3. Begin TDD cycle starting with tokenizer tests
4. Commit after each passing component
5. Final integration and acceptance testing
