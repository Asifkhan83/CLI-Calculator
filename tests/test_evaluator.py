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


# =============================================================================
# T040: Number evaluation
# =============================================================================


class TestNumberEvaluation:
    """Test evaluation of number nodes."""

    def test_single_number(self):
        """Evaluator should return value of single number."""
        from calculator import Tokenizer, Parser, Evaluator

        tokens = Tokenizer("42").tokenize()
        ast = Parser(tokens).parse()
        result = Evaluator().evaluate(ast)
        assert result == 42

    def test_large_number(self):
        """Evaluator should handle large numbers."""
        from calculator import Tokenizer, Parser, Evaluator

        tokens = Tokenizer("999999999").tokenize()
        ast = Parser(tokens).parse()
        result = Evaluator().evaluate(ast)
        assert result == 999999999

    def test_zero(self):
        """Evaluator should handle zero."""
        from calculator import Tokenizer, Parser, Evaluator

        tokens = Tokenizer("0").tokenize()
        ast = Parser(tokens).parse()
        result = Evaluator().evaluate(ast)
        assert result == 0


# =============================================================================
# T041: Basic arithmetic (+, -, *, /)
# =============================================================================


class TestBasicArithmetic:
    """Test evaluation of basic arithmetic operations."""

    def test_addition(self):
        """Evaluator should compute 5 + 3 = 8."""
        from calculator import Tokenizer, Parser, Evaluator

        tokens = Tokenizer("5 + 3").tokenize()
        ast = Parser(tokens).parse()
        result = Evaluator().evaluate(ast)
        assert result == 8

    def test_subtraction(self):
        """Evaluator should compute 10 - 4 = 6."""
        from calculator import Tokenizer, Parser, Evaluator

        tokens = Tokenizer("10 - 4").tokenize()
        ast = Parser(tokens).parse()
        result = Evaluator().evaluate(ast)
        assert result == 6

    def test_multiplication(self):
        """Evaluator should compute 6 * 7 = 42."""
        from calculator import Tokenizer, Parser, Evaluator

        tokens = Tokenizer("6 * 7").tokenize()
        ast = Parser(tokens).parse()
        result = Evaluator().evaluate(ast)
        assert result == 42

    def test_division(self):
        """Evaluator should compute 20 / 4 = 5."""
        from calculator import Tokenizer, Parser, Evaluator

        tokens = Tokenizer("20 / 4").tokenize()
        ast = Parser(tokens).parse()
        result = Evaluator().evaluate(ast)
        assert result == 5

    def test_chained_subtraction(self):
        """Evaluator should compute 10 - 5 - 2 = 3 (left-to-right)."""
        from calculator import Tokenizer, Parser, Evaluator

        tokens = Tokenizer("10 - 5 - 2").tokenize()
        ast = Parser(tokens).parse()
        result = Evaluator().evaluate(ast)
        assert result == 3  # NOT 7

    def test_long_chained_subtraction(self):
        """Evaluator should compute 20 - 10 - 5 - 3 = 2."""
        from calculator import Tokenizer, Parser, Evaluator

        tokens = Tokenizer("20 - 10 - 5 - 3").tokenize()
        ast = Parser(tokens).parse()
        result = Evaluator().evaluate(ast)
        assert result == 2


# =============================================================================
# T042: Integer division truncation toward zero
# =============================================================================


class TestIntegerDivisionTruncation:
    """Test integer division truncation toward zero.

    CRITICAL: Python's // operator does floor division (toward negative infinity).
    We need truncation toward zero using int(a / b).

    Examples:
    - 15 / 2 = 7 (not 7.5)
    - -7 / 2 = -3 (not -4 which is floor)
    - 7 / -2 = -3 (not -4 which is floor)
    - -7 / -2 = 3 (not 4)
    """

    def test_positive_division_truncation(self):
        """15 / 2 should equal 7 (truncated, not 7.5)."""
        from calculator import Tokenizer, Parser, Evaluator

        tokens = Tokenizer("15 / 2").tokenize()
        ast = Parser(tokens).parse()
        result = Evaluator().evaluate(ast)
        assert result == 7

    def test_negative_dividend_truncation(self):
        """-7 / 2 should equal -3 (truncated toward zero, not -4)."""
        from calculator import Tokenizer, Parser, Evaluator

        tokens = Tokenizer("-7 / 2").tokenize()
        ast = Parser(tokens).parse()
        result = Evaluator().evaluate(ast)
        assert result == -3  # NOT -4 (which is floor)

    def test_negative_divisor_truncation(self):
        """7 / -2 should equal -3 (truncated toward zero, not -4)."""
        from calculator import Tokenizer, Parser, Evaluator

        tokens = Tokenizer("7 / -2").tokenize()
        ast = Parser(tokens).parse()
        result = Evaluator().evaluate(ast)
        assert result == -3  # NOT -4 (which is floor)

    def test_both_negative_truncation(self):
        """-7 / -2 should equal 3 (truncated toward zero)."""
        from calculator import Tokenizer, Parser, Evaluator

        tokens = Tokenizer("-7 / -2").tokenize()
        ast = Parser(tokens).parse()
        result = Evaluator().evaluate(ast)
        assert result == 3

    def test_exact_division(self):
        """20 / 4 should equal 5 (exact division)."""
        from calculator import Tokenizer, Parser, Evaluator

        tokens = Tokenizer("20 / 4").tokenize()
        ast = Parser(tokens).parse()
        result = Evaluator().evaluate(ast)
        assert result == 5

    def test_chained_division(self):
        """100 / 10 / 2 should equal 5."""
        from calculator import Tokenizer, Parser, Evaluator

        tokens = Tokenizer("100 / 10 / 2").tokenize()
        ast = Parser(tokens).parse()
        result = Evaluator().evaluate(ast)
        assert result == 5

    def test_chained_division_2(self):
        """20 / 4 / 2 should equal 2."""
        from calculator import Tokenizer, Parser, Evaluator

        tokens = Tokenizer("20 / 4 / 2").tokenize()
        ast = Parser(tokens).parse()
        result = Evaluator().evaluate(ast)
        assert result == 2


# =============================================================================
# T043: Division by zero raises DivisionByZeroError
# =============================================================================


class TestDivisionByZero:
    """Test division by zero error handling."""

    def test_simple_division_by_zero(self):
        """10 / 0 should raise DivisionByZeroError."""
        from calculator import Tokenizer, Parser, Evaluator, DivisionByZeroError

        tokens = Tokenizer("10 / 0").tokenize()
        ast = Parser(tokens).parse()
        with pytest.raises(DivisionByZeroError):
            Evaluator().evaluate(ast)

    def test_division_by_zero_in_expression(self):
        """5 + 10 / 0 should raise DivisionByZeroError."""
        from calculator import Tokenizer, Parser, Evaluator, DivisionByZeroError

        tokens = Tokenizer("5 + 10 / 0").tokenize()
        ast = Parser(tokens).parse()
        with pytest.raises(DivisionByZeroError):
            Evaluator().evaluate(ast)

    def test_division_by_zero_computed(self):
        """10 / (5 - 5) would be division by zero if we had parentheses.

        For now, test 10 / 0 directly.
        """
        from calculator import Tokenizer, Parser, Evaluator, DivisionByZeroError

        tokens = Tokenizer("10 / 0").tokenize()
        ast = Parser(tokens).parse()
        with pytest.raises(DivisionByZeroError):
            Evaluator().evaluate(ast)


# =============================================================================
# T044: Unary minus evaluation
# =============================================================================


class TestUnaryMinusEvaluation:
    """Test evaluation of unary minus."""

    def test_simple_negation(self):
        """-5 should evaluate to -5."""
        from calculator import Tokenizer, Parser, Evaluator

        tokens = Tokenizer("-5").tokenize()
        ast = Parser(tokens).parse()
        result = Evaluator().evaluate(ast)
        assert result == -5

    def test_negation_in_addition(self):
        """-5 + 3 should evaluate to -2."""
        from calculator import Tokenizer, Parser, Evaluator

        tokens = Tokenizer("-5 + 3").tokenize()
        ast = Parser(tokens).parse()
        result = Evaluator().evaluate(ast)
        assert result == -2

    def test_negation_after_operator(self):
        """5 + -3 should evaluate to 2."""
        from calculator import Tokenizer, Parser, Evaluator

        tokens = Tokenizer("5 + -3").tokenize()
        ast = Parser(tokens).parse()
        result = Evaluator().evaluate(ast)
        assert result == 2

    def test_negation_in_multiplication(self):
        """5 * -3 should evaluate to -15."""
        from calculator import Tokenizer, Parser, Evaluator

        tokens = Tokenizer("5 * -3").tokenize()
        ast = Parser(tokens).parse()
        result = Evaluator().evaluate(ast)
        assert result == -15

    def test_double_negation_via_subtraction(self):
        """5 - -3 should evaluate to 8."""
        from calculator import Tokenizer, Parser, Evaluator

        tokens = Tokenizer("5 - -3").tokenize()
        ast = Parser(tokens).parse()
        result = Evaluator().evaluate(ast)
        assert result == 8


# =============================================================================
# T045: Complex expressions with operator precedence
# =============================================================================


class TestComplexExpressions:
    """Test evaluation of complex expressions with BODMAS precedence."""

    def test_bodmas_precedence(self):
        """2 + 3 * 4 should equal 14 (not 20)."""
        from calculator import Tokenizer, Parser, Evaluator

        tokens = Tokenizer("2 + 3 * 4").tokenize()
        ast = Parser(tokens).parse()
        result = Evaluator().evaluate(ast)
        assert result == 14

    def test_division_before_subtraction(self):
        """10 - 6 / 2 should equal 7 (not 2)."""
        from calculator import Tokenizer, Parser, Evaluator

        tokens = Tokenizer("10 - 6 / 2").tokenize()
        ast = Parser(tokens).parse()
        result = Evaluator().evaluate(ast)
        assert result == 7

    def test_complex_bodmas(self):
        """2 * 3 + 4 * 5 should equal 26."""
        from calculator import Tokenizer, Parser, Evaluator

        tokens = Tokenizer("2 * 3 + 4 * 5").tokenize()
        ast = Parser(tokens).parse()
        result = Evaluator().evaluate(ast)
        assert result == 26

    def test_all_operators(self):
        """1 + 2 - 3 * 4 / 2 should equal -3.

        = 1 + 2 - (3 * 4 / 2)
        = 1 + 2 - (12 / 2)
        = 1 + 2 - 6
        = 3 - 6
        = -3
        """
        from calculator import Tokenizer, Parser, Evaluator

        tokens = Tokenizer("1 + 2 - 3 * 4 / 2").tokenize()
        ast = Parser(tokens).parse()
        result = Evaluator().evaluate(ast)
        assert result == -3

    def test_complex_with_negatives(self):
        """-5 + -3 * -2 should equal 1.

        = (-5) + ((-3) * (-2))
        = -5 + 6
        = 1
        """
        from calculator import Tokenizer, Parser, Evaluator

        tokens = Tokenizer("-5 + -3 * -2").tokenize()
        ast = Parser(tokens).parse()
        result = Evaluator().evaluate(ast)
        assert result == 1

    def test_subtraction_chain_with_bodmas(self):
        """10 - 3 - 2 should equal 5 (left-to-right).

        Per User Story 2, scenario 6.
        """
        from calculator import Tokenizer, Parser, Evaluator

        tokens = Tokenizer("10 - 3 - 2").tokenize()
        ast = Parser(tokens).parse()
        result = Evaluator().evaluate(ast)
        assert result == 5  # NOT 9 (which would be 10 - (3 - 2))
