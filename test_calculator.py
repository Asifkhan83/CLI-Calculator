"""Tests for CLI Calculator."""
import pytest

from calculator import (
    calculate,
    DivisionByZeroError,
    InvalidInputError,
)


class TestBasicOperations:
    """Test basic arithmetic operations."""

    def test_addition(self) -> None:
        assert calculate("2 + 3") == 5
        assert calculate("10 + 20") == 30
        assert calculate("0 + 0") == 0

    def test_subtraction(self) -> None:
        assert calculate("5 - 3") == 2
        assert calculate("10 - 20") == -10
        assert calculate("0 - 0") == 0

    def test_multiplication(self) -> None:
        assert calculate("2 * 3") == 6
        assert calculate("10 * 0") == 0
        assert calculate("7 * 1") == 7

    def test_division(self) -> None:
        assert calculate("6 / 2") == 3
        assert calculate("10 / 3") == 3  # Integer division
        assert calculate("0 / 5") == 0


class TestBODMAS:
    """Test BODMAS/operator precedence."""

    def test_multiplication_before_addition(self) -> None:
        assert calculate("2 + 3 * 4") == 14
        assert calculate("3 * 4 + 2") == 14

    def test_division_before_subtraction(self) -> None:
        assert calculate("10 - 6 / 2") == 7
        assert calculate("6 / 2 - 1") == 2

    def test_parentheses_override_precedence(self) -> None:
        assert calculate("(2 + 3) * 4") == 20
        assert calculate("2 * (3 + 4)") == 14
        assert calculate("(10 - 6) / 2") == 2

    def test_nested_parentheses(self) -> None:
        assert calculate("((2 + 3) * 4)") == 20
        assert calculate("(2 * (3 + (4 - 2)))") == 10

    def test_complex_expressions(self) -> None:
        assert calculate("2 + 3 * 4 - 6 / 2") == 11
        assert calculate("(2 + 3) * (4 - 1)") == 15
        assert calculate("10 / 2 + 3 * 4") == 17


class TestNegativeNumbers:
    """Test handling of negative numbers."""

    def test_negative_result(self) -> None:
        assert calculate("3 - 5") == -2

    def test_unary_minus(self) -> None:
        assert calculate("-5") == -5
        assert calculate("-5 + 3") == -2

    def test_unary_plus(self) -> None:
        assert calculate("+5") == 5


class TestEdgeCases:
    """Test edge cases and special inputs."""

    def test_single_number(self) -> None:
        assert calculate("42") == 42
        assert calculate("0") == 0

    def test_whitespace_handling(self) -> None:
        assert calculate("  2 + 3  ") == 5
        assert calculate("2+3") == 5
        assert calculate("2  +  3") == 5

    def test_large_numbers(self) -> None:
        assert calculate("1000000 + 1") == 1000001
        assert calculate("999999 * 2") == 1999998


class TestDivisionByZero:
    """Test division by zero error handling."""

    def test_direct_division_by_zero(self) -> None:
        with pytest.raises(DivisionByZeroError):
            calculate("5 / 0")

    def test_division_by_zero_in_expression(self) -> None:
        with pytest.raises(DivisionByZeroError):
            calculate("10 + 5 / 0")

    def test_division_by_zero_with_parentheses(self) -> None:
        with pytest.raises(DivisionByZeroError):
            calculate("10 / (5 - 5)")


class TestInvalidInput:
    """Test invalid input error handling."""

    def test_empty_expression(self) -> None:
        with pytest.raises(InvalidInputError):
            calculate("")
        with pytest.raises(InvalidInputError):
            calculate("   ")

    def test_invalid_characters(self) -> None:
        with pytest.raises(InvalidInputError):
            calculate("2 + a")
        with pytest.raises(InvalidInputError):
            calculate("2 $ 3")

    def test_missing_operand(self) -> None:
        with pytest.raises(InvalidInputError):
            calculate("2 +")
        with pytest.raises(InvalidInputError):
            calculate("* 3")

    def test_mismatched_parentheses(self) -> None:
        with pytest.raises(InvalidInputError):
            calculate("(2 + 3")
        with pytest.raises(InvalidInputError):
            calculate("2 + 3)")

    def test_consecutive_operators(self) -> None:
        with pytest.raises(InvalidInputError):
            calculate("2 + * 3")
