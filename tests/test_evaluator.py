"""
Evaluator Component Tests

Tests for the Evaluator class that walks the AST and computes results.
Following TDD approach: tests written FIRST, verified to FAIL, then implementation.

Test Coverage:
- T040: Number evaluation
- T041: Basic arithmetic (+, -, *, /)
- T042: Integer division truncation toward zero (15 / 2 = 7, -7 / 2 = -3)
- T043: Division by zero raises DivisionByZeroError
- T044: Unary minus evaluation
- T045: Complex expressions with operator precedence
"""

import pytest

# Tests will be implemented in Phase 2 (RED phase)
