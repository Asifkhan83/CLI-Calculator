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

    pass


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
