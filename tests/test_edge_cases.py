"""
Edge Case Tests

Tests for edge cases and error handling across all components.
Following TDD approach: tests written FIRST, verified to FAIL, then implementation.

Test Coverage:
- T079-T086: User Story 2 - BODMAS precedence verification
- T097-T111: User Story 4 - Invalid input handling
- Negative operand combinations
- Chained operations
- All error types with specific messages
"""

import pytest
import subprocess
import sys
from pathlib import Path


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
# T079-T086: User Story 2 - BODMAS precedence CLI verification
# =============================================================================


class TestBODMASPrecedenceVerification:
    """Verify BODMAS precedence in CLI (User Story 2)."""

    def test_multiplication_before_addition(self):
        """2 + 3 * 4 should equal 14 (not 20)."""
        exit_code, stdout, stderr = run_calculator("2 + 3 * 4")
        assert exit_code == 0
        assert stdout == "14"
        assert stderr == ""

    def test_division_before_subtraction(self):
        """10 - 6 / 2 should equal 7 (not 2)."""
        exit_code, stdout, stderr = run_calculator("10 - 6 / 2")
        assert exit_code == 0
        assert stdout == "7"
        assert stderr == ""

    def test_complex_bodmas(self):
        """2 * 3 + 4 * 5 should equal 26."""
        exit_code, stdout, stderr = run_calculator("2 * 3 + 4 * 5")
        assert exit_code == 0
        assert stdout == "26"
        assert stderr == ""

    def test_chained_division(self):
        """100 / 10 / 2 should equal 5 (left-to-right)."""
        exit_code, stdout, stderr = run_calculator("100 / 10 / 2")
        assert exit_code == 0
        assert stdout == "5"
        assert stderr == ""

    def test_chained_division_2(self):
        """20 / 4 / 2 should equal 2 (left-to-right)."""
        exit_code, stdout, stderr = run_calculator("20 / 4 / 2")
        assert exit_code == 0
        assert stdout == "2"
        assert stderr == ""

    def test_subtraction_left_to_right(self):
        """10 - 3 - 2 should equal 5 (not 9)."""
        exit_code, stdout, stderr = run_calculator("10 - 3 - 2")
        assert exit_code == 0
        assert stdout == "5"
        assert stderr == ""


# =============================================================================
# T097-T100: User Story 4 - Invalid input handling
# =============================================================================


class TestInvalidOperands:
    """Test handling of invalid operands (User Story 4)."""

    def test_letters_in_expression(self):
        """calculator '5 + abc' should output error to stderr, exit 1."""
        exit_code, stdout, stderr = run_calculator("5 + abc")
        assert exit_code == 1
        assert stdout == ""
        assert "Error:" in stderr

    def test_decimal_number(self):
        """calculator '5.5 + 3' should output error to stderr, exit 1."""
        exit_code, stdout, stderr = run_calculator("5.5 + 3")
        assert exit_code == 1
        assert stdout == ""
        assert "Error:" in stderr


class TestEmptyInput:
    """Test handling of empty/whitespace input (User Story 4)."""

    def test_empty_string(self):
        """calculator '' should output error to stderr, exit 1."""
        exit_code, stdout, stderr = run_calculator("")
        assert exit_code == 1
        assert stdout == ""
        assert "Error:" in stderr

    def test_whitespace_only(self):
        """calculator '   ' should output error to stderr, exit 1."""
        exit_code, stdout, stderr = run_calculator("   ")
        assert exit_code == 1
        assert stdout == ""
        assert "Error:" in stderr


class TestMalformedExpressions:
    """Test handling of malformed expressions (User Story 4)."""

    def test_trailing_operator(self):
        """calculator '5 +' should output error to stderr, exit 1."""
        exit_code, stdout, stderr = run_calculator("5 +")
        assert exit_code == 1
        assert stdout == ""
        assert "Error:" in stderr

    def test_leading_non_minus_operator(self):
        """calculator '+ 5' should output error to stderr, exit 1."""
        exit_code, stdout, stderr = run_calculator("+ 5")
        assert exit_code == 1
        assert stdout == ""
        assert "Error:" in stderr

    def test_double_operator(self):
        """calculator '5 + + 3' should output error to stderr, exit 1."""
        exit_code, stdout, stderr = run_calculator("5 + + 3")
        assert exit_code == 1
        assert stdout == ""
        assert "Error:" in stderr


class TestInvalidOperators:
    """Test handling of invalid operators (User Story 4)."""

    def test_at_sign_operator(self):
        """calculator '5 @ 3' should output error to stderr, exit 1."""
        exit_code, stdout, stderr = run_calculator("5 @ 3")
        assert exit_code == 1
        assert stdout == ""
        assert "Error:" in stderr

    def test_hash_operator(self):
        """calculator '5 # 3' should output error to stderr, exit 1."""
        exit_code, stdout, stderr = run_calculator("5 # 3")
        assert exit_code == 1
        assert stdout == ""
        assert "Error:" in stderr


# =============================================================================
# Negative operand combinations
# =============================================================================


class TestNegativeOperandCombinations:
    """Test various combinations of negative operands."""

    def test_negative_dividend_positive_divisor(self):
        """-7 / 2 should equal -3 (truncation toward zero)."""
        exit_code, stdout, stderr = run_calculator("-7 / 2")
        assert exit_code == 0
        assert stdout == "-3"
        assert stderr == ""

    def test_positive_dividend_negative_divisor(self):
        """7 / -2 should equal -3 (truncation toward zero)."""
        exit_code, stdout, stderr = run_calculator("7 / -2")
        assert exit_code == 0
        assert stdout == "-3"
        assert stderr == ""

    def test_both_negative(self):
        """-7 / -2 should equal 3 (truncation toward zero)."""
        exit_code, stdout, stderr = run_calculator("-7 / -2")
        assert exit_code == 0
        assert stdout == "3"
        assert stderr == ""

    def test_negative_in_complex_expression(self):
        """-5 + -3 * -2 should equal 1."""
        exit_code, stdout, stderr = run_calculator("-5 + -3 * -2")
        assert exit_code == 0
        assert stdout == "1"
        assert stderr == ""

    def test_unary_minus_at_start(self):
        """-5 should equal -5."""
        exit_code, stdout, stderr = run_calculator("-5")
        assert exit_code == 0
        assert stdout == "-5"
        assert stderr == ""

    def test_subtraction_of_negative(self):
        """5 - -3 should equal 8."""
        exit_code, stdout, stderr = run_calculator("5 - -3")
        assert exit_code == 0
        assert stdout == "8"
        assert stderr == ""


# =============================================================================
# Chained operations
# =============================================================================


class TestChainedOperations:
    """Test chained operations with same precedence (left-to-right)."""

    def test_chained_addition(self):
        """1 + 2 + 3 + 4 should equal 10."""
        exit_code, stdout, stderr = run_calculator("1 + 2 + 3 + 4")
        assert exit_code == 0
        assert stdout == "10"
        assert stderr == ""

    def test_chained_subtraction(self):
        """20 - 5 - 3 - 2 should equal 10."""
        exit_code, stdout, stderr = run_calculator("20 - 5 - 3 - 2")
        assert exit_code == 0
        assert stdout == "10"
        assert stderr == ""

    def test_chained_multiplication(self):
        """2 * 3 * 4 should equal 24."""
        exit_code, stdout, stderr = run_calculator("2 * 3 * 4")
        assert exit_code == 0
        assert stdout == "24"
        assert stderr == ""

    def test_chained_division(self):
        """120 / 2 / 3 / 4 should equal 5."""
        exit_code, stdout, stderr = run_calculator("120 / 2 / 3 / 4")
        assert exit_code == 0
        assert stdout == "5"
        assert stderr == ""


# =============================================================================
# All error types with specific messages
# =============================================================================


class TestErrorMessages:
    """Test that specific error types produce appropriate messages."""

    def test_division_by_zero_message(self):
        """Division by zero should mention 'division by zero'."""
        exit_code, stdout, stderr = run_calculator("10 / 0")
        assert exit_code == 1
        assert "Error:" in stderr
        # Should mention division by zero
        assert "division" in stderr.lower() and "zero" in stderr.lower()

    def test_invalid_character_message(self):
        """Invalid character should produce error message."""
        exit_code, stdout, stderr = run_calculator("5 @ 3")
        assert exit_code == 1
        assert "Error:" in stderr

    def test_empty_expression_message(self):
        """Empty expression should produce error message."""
        exit_code, stdout, stderr = run_calculator("")
        assert exit_code == 1
        assert "Error:" in stderr

    def test_malformed_expression_message(self):
        """Malformed expression should produce error message."""
        exit_code, stdout, stderr = run_calculator("5 +")
        assert exit_code == 1
        assert "Error:" in stderr


# =============================================================================
# Acceptance scenarios from spec.md
# =============================================================================


class TestAcceptanceScenarios:
    """Test all acceptance scenarios from the specification."""

    # User Story 1 acceptance scenarios
    def test_us1_scenario_1(self):
        """US1-1: 5 + 3 = 8"""
        exit_code, stdout, _ = run_calculator("5 + 3")
        assert exit_code == 0
        assert stdout == "8"

    def test_us1_scenario_2(self):
        """US1-2: 10 - 4 = 6"""
        exit_code, stdout, _ = run_calculator("10 - 4")
        assert exit_code == 0
        assert stdout == "6"

    def test_us1_scenario_3(self):
        """US1-3: 6 * 7 = 42"""
        exit_code, stdout, _ = run_calculator("6 * 7")
        assert exit_code == 0
        assert stdout == "42"

    def test_us1_scenario_4(self):
        """US1-4: 20 / 4 = 5"""
        exit_code, stdout, _ = run_calculator("20 / 4")
        assert exit_code == 0
        assert stdout == "5"

    def test_us1_scenario_5(self):
        """US1-5: 15 / 2 = 7 (integer division truncated)"""
        exit_code, stdout, _ = run_calculator("15 / 2")
        assert exit_code == 0
        assert stdout == "7"

    def test_us1_scenario_6(self):
        """US1-6: 10 - 5 - 2 = 3 (left-to-right)"""
        exit_code, stdout, _ = run_calculator("10 - 5 - 2")
        assert exit_code == 0
        assert stdout == "3"

    def test_us1_scenario_7(self):
        """US1-7: 20 - 10 - 5 - 3 = 2 (chained subtraction)"""
        exit_code, stdout, _ = run_calculator("20 - 10 - 5 - 3")
        assert exit_code == 0
        assert stdout == "2"

    # User Story 2 acceptance scenarios
    def test_us2_scenario_1(self):
        """US2-1: 2 + 3 * 4 = 14 (multiplication before addition)"""
        exit_code, stdout, _ = run_calculator("2 + 3 * 4")
        assert exit_code == 0
        assert stdout == "14"

    def test_us2_scenario_2(self):
        """US2-2: 10 - 6 / 2 = 7 (division before subtraction)"""
        exit_code, stdout, _ = run_calculator("10 - 6 / 2")
        assert exit_code == 0
        assert stdout == "7"

    def test_us2_scenario_3(self):
        """US2-3: 2 * 3 + 4 * 5 = 26"""
        exit_code, stdout, _ = run_calculator("2 * 3 + 4 * 5")
        assert exit_code == 0
        assert stdout == "26"

    def test_us2_scenario_4(self):
        """US2-4: 100 / 10 / 2 = 5 (left-to-right division)"""
        exit_code, stdout, _ = run_calculator("100 / 10 / 2")
        assert exit_code == 0
        assert stdout == "5"

    def test_us2_scenario_5(self):
        """US2-5: 20 / 4 / 2 = 2 (chained division)"""
        exit_code, stdout, _ = run_calculator("20 / 4 / 2")
        assert exit_code == 0
        assert stdout == "2"

    def test_us2_scenario_6(self):
        """US2-6: 10 - 3 - 2 = 5 (subtraction left-to-right, not 9)"""
        exit_code, stdout, _ = run_calculator("10 - 3 - 2")
        assert exit_code == 0
        assert stdout == "5"

    # User Story 3 acceptance scenarios
    def test_us3_scenario_1(self):
        """US3-1: 10 / 0 should error"""
        exit_code, _, stderr = run_calculator("10 / 0")
        assert exit_code == 1
        assert "Error:" in stderr

    def test_us3_scenario_2(self):
        """US3-2: 5 + 10 / 0 should error"""
        exit_code, _, stderr = run_calculator("5 + 10 / 0")
        assert exit_code == 1
        assert "Error:" in stderr
