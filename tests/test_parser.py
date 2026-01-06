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


# =============================================================================
# T023: Simple addition (5 + 3)
# =============================================================================


class TestSimpleAddition:
    """Test parsing of simple addition expressions."""

    def test_simple_addition(self):
        """Parser should create correct AST for 5 + 3."""
        from calculator import Tokenizer, Parser, NumberNode, BinaryOpNode, TokenType

        tokens = Tokenizer("5 + 3").tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        assert isinstance(ast, BinaryOpNode)
        assert ast.operator == TokenType.PLUS
        assert isinstance(ast.left, NumberNode)
        assert ast.left.value == 5
        assert isinstance(ast.right, NumberNode)
        assert ast.right.value == 3

    def test_addition_multiple_terms(self):
        """Parser should handle 1 + 2 + 3 with left-to-right associativity."""
        from calculator import Tokenizer, Parser, NumberNode, BinaryOpNode, TokenType

        tokens = Tokenizer("1 + 2 + 3").tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        # Should be ((1 + 2) + 3)
        assert isinstance(ast, BinaryOpNode)
        assert ast.operator == TokenType.PLUS
        assert isinstance(ast.left, BinaryOpNode)
        assert isinstance(ast.right, NumberNode)
        assert ast.right.value == 3


# =============================================================================
# T024: Simple subtraction, multiplication, division
# =============================================================================


class TestSimpleOperations:
    """Test parsing of simple arithmetic operations."""

    def test_simple_subtraction(self):
        """Parser should create correct AST for 10 - 4."""
        from calculator import Tokenizer, Parser, NumberNode, BinaryOpNode, TokenType

        tokens = Tokenizer("10 - 4").tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        assert isinstance(ast, BinaryOpNode)
        assert ast.operator == TokenType.MINUS
        assert isinstance(ast.left, NumberNode)
        assert ast.left.value == 10
        assert isinstance(ast.right, NumberNode)
        assert ast.right.value == 4

    def test_simple_multiplication(self):
        """Parser should create correct AST for 6 * 7."""
        from calculator import Tokenizer, Parser, NumberNode, BinaryOpNode, TokenType

        tokens = Tokenizer("6 * 7").tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        assert isinstance(ast, BinaryOpNode)
        assert ast.operator == TokenType.MULTIPLY
        assert isinstance(ast.left, NumberNode)
        assert ast.left.value == 6
        assert isinstance(ast.right, NumberNode)
        assert ast.right.value == 7

    def test_simple_division(self):
        """Parser should create correct AST for 20 / 4."""
        from calculator import Tokenizer, Parser, NumberNode, BinaryOpNode, TokenType

        tokens = Tokenizer("20 / 4").tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        assert isinstance(ast, BinaryOpNode)
        assert ast.operator == TokenType.DIVIDE
        assert isinstance(ast.left, NumberNode)
        assert ast.left.value == 20
        assert isinstance(ast.right, NumberNode)
        assert ast.right.value == 4


# =============================================================================
# T025: BODMAS precedence (2 + 3 * 4 = 14)
# =============================================================================


class TestBODMASPrecedence:
    """Test BODMAS operator precedence in parser."""

    def test_multiplication_before_addition(self):
        """Parser should give multiplication higher precedence than addition.

        2 + 3 * 4 should parse as 2 + (3 * 4), not (2 + 3) * 4
        """
        from calculator import Tokenizer, Parser, NumberNode, BinaryOpNode, TokenType

        tokens = Tokenizer("2 + 3 * 4").tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        # Should be 2 + (3 * 4)
        assert isinstance(ast, BinaryOpNode)
        assert ast.operator == TokenType.PLUS
        assert isinstance(ast.left, NumberNode)
        assert ast.left.value == 2
        assert isinstance(ast.right, BinaryOpNode)
        assert ast.right.operator == TokenType.MULTIPLY

    def test_division_before_subtraction(self):
        """Parser should give division higher precedence than subtraction.

        10 - 6 / 2 should parse as 10 - (6 / 2)
        """
        from calculator import Tokenizer, Parser, NumberNode, BinaryOpNode, TokenType

        tokens = Tokenizer("10 - 6 / 2").tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        # Should be 10 - (6 / 2)
        assert isinstance(ast, BinaryOpNode)
        assert ast.operator == TokenType.MINUS
        assert isinstance(ast.left, NumberNode)
        assert ast.left.value == 10
        assert isinstance(ast.right, BinaryOpNode)
        assert ast.right.operator == TokenType.DIVIDE

    def test_complex_bodmas(self):
        """Parser should handle complex expressions: 2 * 3 + 4 * 5."""
        from calculator import Tokenizer, Parser, BinaryOpNode, TokenType

        tokens = Tokenizer("2 * 3 + 4 * 5").tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        # Should be (2 * 3) + (4 * 5)
        assert isinstance(ast, BinaryOpNode)
        assert ast.operator == TokenType.PLUS
        assert isinstance(ast.left, BinaryOpNode)
        assert ast.left.operator == TokenType.MULTIPLY
        assert isinstance(ast.right, BinaryOpNode)
        assert ast.right.operator == TokenType.MULTIPLY


# =============================================================================
# T026: Left-to-right associativity (10 - 5 - 2 = 3)
# =============================================================================


class TestLeftToRightAssociativity:
    """Test left-to-right associativity for same-precedence operators."""

    def test_subtraction_left_to_right(self):
        """Parser should parse 10 - 5 - 2 as ((10 - 5) - 2).

        This is critical: 10 - 5 - 2 = 3, NOT 10 - (5 - 2) = 7
        """
        from calculator import Tokenizer, Parser, NumberNode, BinaryOpNode, TokenType

        tokens = Tokenizer("10 - 5 - 2").tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        # Should be ((10 - 5) - 2)
        assert isinstance(ast, BinaryOpNode)
        assert ast.operator == TokenType.MINUS
        assert isinstance(ast.left, BinaryOpNode)  # (10 - 5)
        assert isinstance(ast.right, NumberNode)
        assert ast.right.value == 2

    def test_division_left_to_right(self):
        """Parser should parse 100 / 10 / 2 as ((100 / 10) / 2).

        100 / 10 / 2 = 5, NOT 100 / (10 / 2) = 20
        """
        from calculator import Tokenizer, Parser, NumberNode, BinaryOpNode, TokenType

        tokens = Tokenizer("100 / 10 / 2").tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        # Should be ((100 / 10) / 2)
        assert isinstance(ast, BinaryOpNode)
        assert ast.operator == TokenType.DIVIDE
        assert isinstance(ast.left, BinaryOpNode)  # (100 / 10)
        assert isinstance(ast.right, NumberNode)
        assert ast.right.value == 2

    def test_chained_subtraction(self):
        """Parser should handle 20 - 10 - 5 - 3 correctly."""
        from calculator import Tokenizer, Parser, NumberNode, BinaryOpNode, TokenType

        tokens = Tokenizer("20 - 10 - 5 - 3").tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        # Should be (((20 - 10) - 5) - 3)
        assert isinstance(ast, BinaryOpNode)
        assert ast.operator == TokenType.MINUS
        assert isinstance(ast.right, NumberNode)
        assert ast.right.value == 3


# =============================================================================
# T027: Unary minus at start and after operators
# =============================================================================


class TestUnaryMinusParsing:
    """Test parsing of unary minus in various contexts."""

    def test_unary_minus_at_start(self):
        """Parser should handle -5 as unary minus."""
        from calculator import Tokenizer, Parser, NumberNode, UnaryOpNode, TokenType

        tokens = Tokenizer("-5").tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        assert isinstance(ast, UnaryOpNode)
        assert ast.operator == TokenType.MINUS
        assert isinstance(ast.operand, NumberNode)
        assert ast.operand.value == 5

    def test_unary_minus_in_expression(self):
        """Parser should handle -5 + 3."""
        from calculator import Tokenizer, Parser, UnaryOpNode, BinaryOpNode, TokenType

        tokens = Tokenizer("-5 + 3").tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        assert isinstance(ast, BinaryOpNode)
        assert ast.operator == TokenType.PLUS
        assert isinstance(ast.left, UnaryOpNode)

    def test_unary_minus_after_operator(self):
        """Parser should handle 5 + -3."""
        from calculator import Tokenizer, Parser, UnaryOpNode, BinaryOpNode, TokenType

        tokens = Tokenizer("5 + -3").tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        assert isinstance(ast, BinaryOpNode)
        assert ast.operator == TokenType.PLUS
        assert isinstance(ast.right, UnaryOpNode)

    def test_unary_minus_after_multiply(self):
        """Parser should handle 5 * -3."""
        from calculator import Tokenizer, Parser, UnaryOpNode, BinaryOpNode, TokenType

        tokens = Tokenizer("5 * -3").tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        assert isinstance(ast, BinaryOpNode)
        assert ast.operator == TokenType.MULTIPLY
        assert isinstance(ast.right, UnaryOpNode)

    def test_complex_unary_minus(self):
        """Parser should handle -5 + -3 * -2."""
        from calculator import Tokenizer, Parser, UnaryOpNode, BinaryOpNode, TokenType

        tokens = Tokenizer("-5 + -3 * -2").tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        # Should be (-5) + ((-3) * (-2))
        assert isinstance(ast, BinaryOpNode)
        assert ast.operator == TokenType.PLUS


# =============================================================================
# T028: Malformed expressions raise errors
# =============================================================================


class TestMalformedExpressions:
    """Test that malformed expressions raise appropriate errors."""

    def test_operator_at_end(self):
        """Parser should raise error for expression ending with operator."""
        from calculator import Tokenizer, Parser, MalformedExpressionError

        tokens = Tokenizer("5 +").tokenize()
        parser = Parser(tokens)
        with pytest.raises(MalformedExpressionError):
            parser.parse()

    def test_double_operator(self):
        """Parser should raise error for double operators (not unary context)."""
        from calculator import Tokenizer, Parser, MalformedExpressionError

        tokens = Tokenizer("5 + +").tokenize()
        parser = Parser(tokens)
        with pytest.raises(MalformedExpressionError):
            parser.parse()

    def test_operator_at_start_non_minus(self):
        """Parser should raise error for expression starting with non-minus operator."""
        from calculator import Tokenizer, Parser, MalformedExpressionError

        tokens = Tokenizer("+ 5").tokenize()
        parser = Parser(tokens)
        with pytest.raises(MalformedExpressionError):
            parser.parse()

    def test_missing_operand(self):
        """Parser should raise error for missing operand."""
        from calculator import Tokenizer, Parser, MalformedExpressionError

        tokens = Tokenizer("5 * / 3").tokenize()
        parser = Parser(tokens)
        with pytest.raises(MalformedExpressionError):
            parser.parse()


# =============================================================================
# T029: Empty token list raises error
# =============================================================================


class TestEmptyTokenList:
    """Test that empty or EOF-only token lists raise errors."""

    def test_eof_only(self):
        """Parser should raise error for EOF-only token list."""
        from calculator import Parser, Token, TokenType, MalformedExpressionError

        tokens = [Token(TokenType.EOF)]
        parser = Parser(tokens)
        with pytest.raises(MalformedExpressionError):
            parser.parse()

    def test_empty_list(self):
        """Parser should raise error for empty token list."""
        from calculator import Parser, MalformedExpressionError

        parser = Parser([])
        with pytest.raises(MalformedExpressionError):
            parser.parse()
