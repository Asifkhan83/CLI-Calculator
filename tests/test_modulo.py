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

    pass


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
