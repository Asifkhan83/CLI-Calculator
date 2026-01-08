"""Tests for modulo operator functionality."""
import pytest

from calculator import (
    calculate,
    CalculatorError,
    DivisionByZeroError,
    InvalidInputError,
    ModuloByZeroError,
)


class TestBasicModulo:
    """Tests for basic modulo calculation (US1)."""

    def test_basic_modulo_10_mod_3(self) -> None:
        """Test 10 % 3 = 1."""
        assert calculate("10 % 3") == 1

    def test_basic_modulo_15_mod_5(self) -> None:
        """Test 15 % 5 = 0 (no remainder)."""
        assert calculate("15 % 5") == 0

    def test_basic_modulo_7_mod_4(self) -> None:
        """Test 7 % 4 = 3."""
        assert calculate("7 % 4") == 3

    def test_basic_modulo_100_mod_7(self) -> None:
        """Test 100 % 7 = 2."""
        assert calculate("100 % 7") == 2


class TestModuloPrecedence:
    """Tests for BODMAS precedence with modulo (US2)."""

    def test_modulo_before_addition(self) -> None:
        """Test 10 + 7 % 3 = 11 (modulo evaluated before addition)."""
        assert calculate("10 + 7 % 3") == 11

    def test_modulo_before_subtraction(self) -> None:
        """Test 20 - 10 % 3 = 19 (modulo evaluated before subtraction)."""
        assert calculate("20 - 10 % 3") == 19

    def test_modulo_left_to_right_with_multiply(self) -> None:
        """Test 2 * 10 % 3 = 2 (left-to-right: 20 % 3 = 2)."""
        assert calculate("2 * 10 % 3") == 2

    def test_modulo_left_to_right_modulo_first(self) -> None:
        """Test 10 % 3 * 2 = 2 (left-to-right: 1 * 2 = 2)."""
        assert calculate("10 % 3 * 2") == 2

    def test_modulo_left_to_right_with_divide(self) -> None:
        """Test 15 / 3 % 2 = 1 (left-to-right: 5 % 2 = 1)."""
        assert calculate("15 / 3 % 2") == 1


class TestModuloByZero:
    """Tests for modulo by zero error handling (US3)."""

    def test_modulo_by_zero_error_exists(self) -> None:
        """Test that ModuloByZeroError exception class exists and is a CalculatorError."""
        assert issubclass(ModuloByZeroError, CalculatorError)


class TestModuloNegativeNumbers:
    """Tests for modulo with negative operands (US4)."""

    pass


class TestModuloEdgeCases:
    """Tests for modulo edge cases."""

    pass
