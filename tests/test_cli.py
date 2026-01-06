"""
CLI Integration Tests

Tests for the CLI interface and main() function.
Following TDD approach: tests written FIRST, verified to FAIL, then implementation.

Test Coverage:
- T057-T059: Error message formatting (foundation)
- T060-T062: Error message lookup
- T065-T078: User Story 1 - Basic arithmetic CLI
"""

import pytest
import subprocess
import sys
from pathlib import Path


# =============================================================================
# T057-T059: Error message formatting tests
# =============================================================================


class TestErrorMessageFormatting:
    """Test error message formatting for different exception types."""

    def test_division_by_zero_message(self):
        """DivisionByZeroError should produce correct message."""
        from calculator import DivisionByZeroError, get_error_message

        error = DivisionByZeroError("test")
        message = get_error_message(error)
        assert message == "Error: Division by zero is not allowed"

    def test_malformed_expression_message(self):
        """MalformedExpressionError should produce correct message."""
        from calculator import MalformedExpressionError, get_error_message

        error = MalformedExpressionError("test")
        message = get_error_message(error)
        assert message == "Error: Malformed expression"

    def test_invalid_operand_message(self):
        """InvalidOperandError should produce correct message."""
        from calculator import InvalidOperandError, get_error_message

        error = InvalidOperandError("test")
        message = get_error_message(error)
        assert message == "Error: Invalid operand"

    def test_invalid_operator_message(self):
        """InvalidOperatorError should produce correct message."""
        from calculator import InvalidOperatorError, get_error_message

        error = InvalidOperatorError("test")
        message = get_error_message(error)
        assert message == "Error: Invalid operator"


# =============================================================================
# T060-T062: Error message lookup tests
# =============================================================================


class TestErrorMessageLookup:
    """Test error message lookup functionality."""

    def test_error_messages_dict_exists(self):
        """ERROR_MESSAGES dictionary should exist."""
        from calculator import ERROR_MESSAGES

        assert isinstance(ERROR_MESSAGES, dict)

    def test_error_messages_contains_all_types(self):
        """ERROR_MESSAGES should contain all exception types."""
        from calculator import (
            ERROR_MESSAGES,
            DivisionByZeroError,
            InvalidOperandError,
            InvalidOperatorError,
            MalformedExpressionError,
        )

        assert DivisionByZeroError in ERROR_MESSAGES
        assert InvalidOperandError in ERROR_MESSAGES
        assert InvalidOperatorError in ERROR_MESSAGES
        assert MalformedExpressionError in ERROR_MESSAGES

    def test_get_error_message_function_exists(self):
        """get_error_message function should exist."""
        from calculator import get_error_message

        assert callable(get_error_message)


# =============================================================================
# Helper for CLI tests
# =============================================================================


def run_calculator(expression: str) -> tuple[int, str, str]:
    """
    Run the calculator CLI with an expression.

    Args:
        expression: The mathematical expression to evaluate.

    Returns:
        Tuple of (exit_code, stdout, stderr).
    """
    result = subprocess.run(
        [sys.executable, "calculator.py", expression],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent,
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()


# =============================================================================
# T065-T067: User Story 1 - Basic arithmetic CLI tests
# =============================================================================


class TestBasicArithmeticCLI:
    """Test CLI for basic arithmetic operations (User Story 1)."""

    def test_addition(self):
        """calculator '5 + 3' should output 8 to stdout, exit 0."""
        exit_code, stdout, stderr = run_calculator("5 + 3")
        assert exit_code == 0
        assert stdout == "8"
        assert stderr == ""

    def test_subtraction(self):
        """calculator '10 - 4' should output 6 to stdout, exit 0."""
        exit_code, stdout, stderr = run_calculator("10 - 4")
        assert exit_code == 0
        assert stdout == "6"
        assert stderr == ""

    def test_multiplication(self):
        """calculator '6 * 7' should output 42 to stdout, exit 0."""
        exit_code, stdout, stderr = run_calculator("6 * 7")
        assert exit_code == 0
        assert stdout == "42"
        assert stderr == ""

    def test_division(self):
        """calculator '20 / 4' should output 5 to stdout, exit 0."""
        exit_code, stdout, stderr = run_calculator("20 / 4")
        assert exit_code == 0
        assert stdout == "5"
        assert stderr == ""


class TestIntegerDivisionCLI:
    """Test CLI for integer division truncation (User Story 1)."""

    def test_integer_division_truncation(self):
        """calculator '15 / 2' should output 7 to stdout, exit 0."""
        exit_code, stdout, stderr = run_calculator("15 / 2")
        assert exit_code == 0
        assert stdout == "7"
        assert stderr == ""

    def test_negative_dividend_truncation(self):
        """calculator '-7 / 2' should output -3 to stdout, exit 0."""
        exit_code, stdout, stderr = run_calculator("-7 / 2")
        assert exit_code == 0
        assert stdout == "-3"
        assert stderr == ""


class TestChainedOperationsCLI:
    """Test CLI for chained operations with left-to-right associativity."""

    def test_subtraction_chain(self):
        """calculator '10 - 5 - 2' should output 3 to stdout, exit 0."""
        exit_code, stdout, stderr = run_calculator("10 - 5 - 2")
        assert exit_code == 0
        assert stdout == "3"
        assert stderr == ""

    def test_long_subtraction_chain(self):
        """calculator '20 - 10 - 5 - 3' should output 2 to stdout, exit 0."""
        exit_code, stdout, stderr = run_calculator("20 - 10 - 5 - 3")
        assert exit_code == 0
        assert stdout == "2"
        assert stderr == ""


# =============================================================================
# T068-T074: CLI implementation tests
# =============================================================================


class TestCLIImplementation:
    """Test CLI interface implementation."""

    def test_exit_code_success(self):
        """Successful calculation should exit with code 0."""
        exit_code, _, _ = run_calculator("1 + 1")
        assert exit_code == 0

    def test_exit_code_error(self):
        """Failed calculation should exit with code 1."""
        exit_code, _, _ = run_calculator("1 / 0")
        assert exit_code == 1

    def test_stdout_for_success(self):
        """Result should go to stdout on success."""
        _, stdout, stderr = run_calculator("2 + 2")
        assert stdout == "4"
        assert stderr == ""

    def test_stderr_for_error(self):
        """Error message should go to stderr on failure."""
        _, stdout, stderr = run_calculator("1 / 0")
        assert stdout == ""
        assert stderr.startswith("Error:")

    def test_calculate_function(self):
        """calculate() function should work correctly."""
        from calculator import calculate

        assert calculate("5 + 3") == 8
        assert calculate("2 + 3 * 4") == 14
        assert calculate("10 - 5 - 2") == 3


# =============================================================================
# BODMAS precedence CLI tests (User Story 2)
# =============================================================================


class TestBODMASPrecedenceCLI:
    """Test CLI for BODMAS operator precedence (User Story 2)."""

    def test_multiplication_before_addition(self):
        """calculator '2 + 3 * 4' should output 14, exit 0."""
        exit_code, stdout, stderr = run_calculator("2 + 3 * 4")
        assert exit_code == 0
        assert stdout == "14"
        assert stderr == ""

    def test_division_before_subtraction(self):
        """calculator '10 - 6 / 2' should output 7, exit 0."""
        exit_code, stdout, stderr = run_calculator("10 - 6 / 2")
        assert exit_code == 0
        assert stdout == "7"
        assert stderr == ""

    def test_complex_bodmas(self):
        """calculator '2 * 3 + 4 * 5' should output 26, exit 0."""
        exit_code, stdout, stderr = run_calculator("2 * 3 + 4 * 5")
        assert exit_code == 0
        assert stdout == "26"
        assert stderr == ""


# =============================================================================
# Division by zero CLI tests (User Story 3)
# =============================================================================


class TestDivisionByZeroCLI:
    """Test CLI for division by zero error handling (User Story 3)."""

    def test_simple_division_by_zero(self):
        """calculator '10 / 0' should output error to stderr, exit 1."""
        exit_code, stdout, stderr = run_calculator("10 / 0")
        assert exit_code == 1
        assert stdout == ""
        assert "Error:" in stderr
        assert "Division by zero" in stderr or "division by zero" in stderr.lower()

    def test_division_by_zero_in_expression(self):
        """calculator '5 + 10 / 0' should output error to stderr, exit 1."""
        exit_code, stdout, stderr = run_calculator("5 + 10 / 0")
        assert exit_code == 1
        assert stdout == ""
        assert "Error:" in stderr
