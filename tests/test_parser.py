"""
Parser Component Tests

Tests for the Parser class that converts tokens into an Abstract Syntax Tree (AST).
Following TDD approach: tests written FIRST, verified to FAIL, then implementation.

Test Coverage:
- T023: Simple addition (5 + 3)
- T024: Simple subtraction, multiplication, division
- T025: BODMAS precedence (2 + 3 * 4 = 14)
- T026: Left-to-right associativity (10 - 5 - 2 = 3)
- T027: Unary minus at start and after operators
- T028: Malformed expressions raise errors
- T029: Empty token list raises error
"""

import pytest

# Tests will be implemented in Phase 2 (RED phase)
