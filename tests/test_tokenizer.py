"""
Tokenizer Component Tests

Tests for the Tokenizer class that converts string input into tokens.
Following TDD approach: tests written FIRST, verified to FAIL, then implementation.

Test Coverage:
- T006: Basic operators (+, -, *, /)
- T007: Positive integers, whitespace handling
- T008: Unary minus detection (start, after operators)
- T009: Invalid characters raise errors
- T010: Empty/whitespace-only input raises errors
"""

import pytest


# =============================================================================
# T006: Basic operators (+, -, *, /)
# =============================================================================


class TestBasicOperators:
    """Test tokenization of basic arithmetic operators."""

    def test_plus_operator(self):
        """Tokenizer should recognize + as PLUS token."""
        from calculator import Tokenizer, TokenType

        tokenizer = Tokenizer("5 + 3")
        tokens = tokenizer.tokenize()
        assert any(t.type == TokenType.PLUS for t in tokens)

    def test_minus_operator(self):
        """Tokenizer should recognize - as MINUS token (binary context)."""
        from calculator import Tokenizer, TokenType

        tokenizer = Tokenizer("5 - 3")
        tokens = tokenizer.tokenize()
        assert any(t.type == TokenType.MINUS for t in tokens)

    def test_multiply_operator(self):
        """Tokenizer should recognize * as MULTIPLY token."""
        from calculator import Tokenizer, TokenType

        tokenizer = Tokenizer("5 * 3")
        tokens = tokenizer.tokenize()
        assert any(t.type == TokenType.MULTIPLY for t in tokens)

    def test_divide_operator(self):
        """Tokenizer should recognize / as DIVIDE token."""
        from calculator import Tokenizer, TokenType

        tokenizer = Tokenizer("5 / 3")
        tokens = tokenizer.tokenize()
        assert any(t.type == TokenType.DIVIDE for t in tokens)

    def test_all_operators_in_expression(self):
        """Tokenizer should handle expression with all operators."""
        from calculator import Tokenizer, TokenType

        tokenizer = Tokenizer("1 + 2 - 3 * 4 / 5")
        tokens = tokenizer.tokenize()
        types = [t.type for t in tokens]
        assert TokenType.PLUS in types
        assert TokenType.MINUS in types
        assert TokenType.MULTIPLY in types
        assert TokenType.DIVIDE in types


# =============================================================================
# T007: Positive integers, whitespace handling
# =============================================================================


class TestNumbersAndWhitespace:
    """Test tokenization of numbers and whitespace handling."""

    def test_single_digit_number(self):
        """Tokenizer should parse single digit numbers."""
        from calculator import Tokenizer, TokenType

        tokenizer = Tokenizer("5")
        tokens = tokenizer.tokenize()
        assert tokens[0].type == TokenType.NUMBER
        assert tokens[0].value == 5

    def test_multi_digit_number(self):
        """Tokenizer should parse multi-digit numbers."""
        from calculator import Tokenizer, TokenType

        tokenizer = Tokenizer("123")
        tokens = tokenizer.tokenize()
        assert tokens[0].type == TokenType.NUMBER
        assert tokens[0].value == 123

    def test_large_number(self):
        """Tokenizer should parse large numbers."""
        from calculator import Tokenizer, TokenType

        tokenizer = Tokenizer("999999999")
        tokens = tokenizer.tokenize()
        assert tokens[0].type == TokenType.NUMBER
        assert tokens[0].value == 999999999

    def test_whitespace_between_tokens(self):
        """Tokenizer should skip whitespace between tokens."""
        from calculator import Tokenizer, TokenType

        tokenizer = Tokenizer("5 + 3")
        tokens = tokenizer.tokenize()
        # Should have: NUMBER(5), PLUS, NUMBER(3), EOF
        assert len([t for t in tokens if t.type != TokenType.EOF]) == 3

    def test_no_whitespace(self):
        """Tokenizer should work without whitespace."""
        from calculator import Tokenizer, TokenType

        tokenizer = Tokenizer("5+3")
        tokens = tokenizer.tokenize()
        assert len([t for t in tokens if t.type != TokenType.EOF]) == 3

    def test_extra_whitespace(self):
        """Tokenizer should handle extra whitespace."""
        from calculator import Tokenizer, TokenType

        tokenizer = Tokenizer("  5   +   3  ")
        tokens = tokenizer.tokenize()
        non_eof = [t for t in tokens if t.type != TokenType.EOF]
        assert len(non_eof) == 3
        assert non_eof[0].value == 5
        assert non_eof[2].value == 3

    def test_eof_token(self):
        """Tokenizer should end with EOF token."""
        from calculator import Tokenizer, TokenType

        tokenizer = Tokenizer("5")
        tokens = tokenizer.tokenize()
        assert tokens[-1].type == TokenType.EOF


# =============================================================================
# T008: Unary minus detection (start, after operators)
# =============================================================================


class TestUnaryMinus:
    """Test unary minus detection in different contexts."""

    def test_unary_minus_at_start(self):
        """Tokenizer should detect unary minus at expression start."""
        from calculator import Tokenizer, TokenType

        tokenizer = Tokenizer("-5")
        tokens = tokenizer.tokenize()
        # Should be: MINUS (unary), NUMBER(5), EOF
        assert tokens[0].type == TokenType.MINUS
        assert tokens[1].type == TokenType.NUMBER
        assert tokens[1].value == 5

    def test_unary_minus_after_plus(self):
        """Tokenizer should detect unary minus after + operator."""
        from calculator import Tokenizer, TokenType

        tokenizer = Tokenizer("5 + -3")
        tokens = tokenizer.tokenize()
        # Should have MINUS token before the 3
        types = [t.type for t in tokens]
        # Find index of second MINUS (unary)
        assert TokenType.MINUS in types

    def test_unary_minus_after_minus(self):
        """Tokenizer should detect unary minus after - operator."""
        from calculator import Tokenizer, TokenType

        tokenizer = Tokenizer("5 - -3")
        tokens = tokenizer.tokenize()
        # Should have two MINUS tokens
        minus_count = sum(1 for t in tokens if t.type == TokenType.MINUS)
        assert minus_count == 2

    def test_unary_minus_after_multiply(self):
        """Tokenizer should detect unary minus after * operator."""
        from calculator import Tokenizer, TokenType

        tokenizer = Tokenizer("5 * -3")
        tokens = tokenizer.tokenize()
        assert any(t.type == TokenType.MINUS for t in tokens)

    def test_unary_minus_after_divide(self):
        """Tokenizer should detect unary minus after / operator."""
        from calculator import Tokenizer, TokenType

        tokenizer = Tokenizer("5 / -3")
        tokens = tokenizer.tokenize()
        assert any(t.type == TokenType.MINUS for t in tokens)

    def test_negative_number_in_complex_expression(self):
        """Tokenizer should handle negative numbers in complex expressions."""
        from calculator import Tokenizer, TokenType

        tokenizer = Tokenizer("-5 + -3 * -2")
        tokens = tokenizer.tokenize()
        # Should have 3 MINUS tokens (all unary)
        minus_count = sum(1 for t in tokens if t.type == TokenType.MINUS)
        assert minus_count == 3


# =============================================================================
# T009: Invalid characters raise errors
# =============================================================================


class TestInvalidCharacters:
    """Test that invalid characters raise appropriate errors."""

    def test_invalid_character_at_sign(self):
        """Tokenizer should raise error for @ character."""
        from calculator import Tokenizer, InvalidOperandError

        tokenizer = Tokenizer("5 @ 3")
        with pytest.raises(InvalidOperandError):
            tokenizer.tokenize()

    def test_invalid_character_hash(self):
        """Tokenizer should raise error for # character."""
        from calculator import Tokenizer, InvalidOperandError

        tokenizer = Tokenizer("5 # 3")
        with pytest.raises(InvalidOperandError):
            tokenizer.tokenize()

    def test_invalid_character_dollar(self):
        """Tokenizer should raise error for $ character."""
        from calculator import Tokenizer, InvalidOperandError

        tokenizer = Tokenizer("5 $ 3")
        with pytest.raises(InvalidOperandError):
            tokenizer.tokenize()

    def test_invalid_character_letter(self):
        """Tokenizer should raise error for letters."""
        from calculator import Tokenizer, InvalidOperandError

        tokenizer = Tokenizer("5 + abc")
        with pytest.raises(InvalidOperandError):
            tokenizer.tokenize()

    def test_invalid_character_decimal_point(self):
        """Tokenizer should raise error for decimal numbers (integers only)."""
        from calculator import Tokenizer, InvalidOperandError

        tokenizer = Tokenizer("5.5 + 3")
        with pytest.raises(InvalidOperandError):
            tokenizer.tokenize()


# =============================================================================
# T010: Empty/whitespace-only input raises errors
# =============================================================================


class TestEmptyInput:
    """Test that empty or whitespace-only input raises errors."""

    def test_empty_string(self):
        """Tokenizer should raise error for empty string."""
        from calculator import Tokenizer, MalformedExpressionError

        tokenizer = Tokenizer("")
        with pytest.raises(MalformedExpressionError):
            tokenizer.tokenize()

    def test_whitespace_only(self):
        """Tokenizer should raise error for whitespace-only input."""
        from calculator import Tokenizer, MalformedExpressionError

        tokenizer = Tokenizer("   ")
        with pytest.raises(MalformedExpressionError):
            tokenizer.tokenize()

    def test_tabs_only(self):
        """Tokenizer should raise error for tabs-only input."""
        from calculator import Tokenizer, MalformedExpressionError

        tokenizer = Tokenizer("\t\t")
        with pytest.raises(MalformedExpressionError):
            tokenizer.tokenize()

    def test_mixed_whitespace_only(self):
        """Tokenizer should raise error for mixed whitespace-only input."""
        from calculator import Tokenizer, MalformedExpressionError

        tokenizer = Tokenizer("  \t  \n  ")
        with pytest.raises(MalformedExpressionError):
            tokenizer.tokenize()
