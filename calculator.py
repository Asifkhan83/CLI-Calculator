#!/usr/bin/env python3
"""
CLI Calculator - Single-file implementation with recursive descent parser.

Supports:
- Integer arithmetic (+, -, *, /)
- BODMAS operator precedence
- Unary minus (at start and after operators)
- Integer division truncating toward zero
- Comprehensive error handling

Usage:
    python calculator.py "<expression>"

Examples:
    python calculator.py "5 + 3"      # outputs: 8
    python calculator.py "2 + 3 * 4"  # outputs: 14
    python calculator.py "10 / 0"     # outputs: Error: Division by zero
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Optional, Union


# =============================================================================
# Custom Exceptions (T046)
# =============================================================================


class CalculatorError(Exception):
    """Base exception for calculator errors."""

    pass


class DivisionByZeroError(CalculatorError):
    """Raised when attempting to divide by zero."""

    pass


class InvalidOperandError(CalculatorError):
    """Raised when an invalid operand is encountered."""

    pass


class InvalidOperatorError(CalculatorError):
    """Raised when an invalid operator is encountered."""

    pass


class MalformedExpressionError(CalculatorError):
    """Raised when the expression is malformed or empty."""

    pass


# =============================================================================
# Token Types and Token Class (T012, T013)
# =============================================================================


class TokenType(Enum):
    """Types of tokens in the calculator language."""

    NUMBER = auto()
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    EOF = auto()


@dataclass
class Token:
    """Represents a token in the input expression."""

    type: TokenType
    value: Optional[int] = None

    def __repr__(self) -> str:
        if self.value is not None:
            return f"Token({self.type.name}, {self.value})"
        return f"Token({self.type.name})"


# =============================================================================
# Tokenizer (T011, T014-T018)
# =============================================================================


class Tokenizer:
    """
    Converts a string expression into a list of tokens.

    The tokenizer handles:
    - Integer numbers (positive)
    - Arithmetic operators: +, -, *, /
    - Whitespace (skipped)
    - Unary minus detection (context-sensitive)

    Args:
        expression: The mathematical expression to tokenize.

    Raises:
        MalformedExpressionError: If the expression is empty or whitespace-only.
        InvalidOperandError: If an invalid character is encountered.
    """

    def __init__(self, expression: str) -> None:
        """Initialize the tokenizer with an expression."""
        self.expression = expression
        self.pos = 0
        self.current_char: Optional[str] = expression[0] if expression else None

    def advance(self) -> None:
        """Move to the next character in the expression."""
        self.pos += 1
        if self.pos < len(self.expression):
            self.current_char = self.expression[self.pos]
        else:
            self.current_char = None

    def skip_whitespace(self) -> None:
        """Skip over whitespace characters."""
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def parse_number(self) -> int:
        """
        Parse a positive integer from the current position.

        Returns:
            The parsed integer value.
        """
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def tokenize(self) -> List[Token]:
        """
        Convert the expression into a list of tokens.

        Returns:
            A list of Token objects representing the expression.

        Raises:
            MalformedExpressionError: If the expression is empty or whitespace-only.
            InvalidOperandError: If an invalid character is encountered.
        """
        tokens: List[Token] = []

        # Check for empty or whitespace-only input
        if not self.expression or self.expression.strip() == "":
            raise MalformedExpressionError("Expression cannot be empty")

        while self.current_char is not None:
            # Skip whitespace
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            # Parse numbers
            if self.current_char.isdigit():
                tokens.append(Token(TokenType.NUMBER, self.parse_number()))
                continue

            # Parse operators
            if self.current_char == "+":
                tokens.append(Token(TokenType.PLUS))
                self.advance()
                continue

            if self.current_char == "-":
                tokens.append(Token(TokenType.MINUS))
                self.advance()
                continue

            if self.current_char == "*":
                tokens.append(Token(TokenType.MULTIPLY))
                self.advance()
                continue

            if self.current_char == "/":
                tokens.append(Token(TokenType.DIVIDE))
                self.advance()
                continue

            # Invalid character
            raise InvalidOperandError(
                f"Invalid character '{self.current_char}' at position {self.pos}"
            )

        # Add EOF token
        tokens.append(Token(TokenType.EOF))
        return tokens


# =============================================================================
# AST Nodes (T030)
# =============================================================================


class ASTNode:
    """Base class for Abstract Syntax Tree nodes."""

    pass


@dataclass
class NumberNode(ASTNode):
    """AST node representing a number."""

    value: int


@dataclass
class BinaryOpNode(ASTNode):
    """AST node representing a binary operation."""

    left: ASTNode
    operator: TokenType
    right: ASTNode


@dataclass
class UnaryOpNode(ASTNode):
    """AST node representing a unary operation (negation)."""

    operator: TokenType
    operand: ASTNode


# =============================================================================
# Parser (T031-T035)
# =============================================================================


class Parser:
    """
    Recursive descent parser for mathematical expressions.

    Grammar (EBNF):
        expression := term ((PLUS | MINUS) term)*
        term       := factor ((MULTIPLY | DIVIDE) factor)*
        factor     := NUMBER | MINUS factor

    The parser implements BODMAS precedence:
    - Multiplication and division have higher precedence than addition/subtraction
    - Left-to-right associativity for operators of the same precedence

    Args:
        tokens: List of tokens to parse.

    Raises:
        MalformedExpressionError: If the token list is empty or the expression is invalid.
    """

    def __init__(self, tokens: List[Token]) -> None:
        """Initialize the parser with a list of tokens."""
        self.tokens = tokens
        self.pos = 0
        self.current_token = tokens[0] if tokens else None

    def advance(self) -> None:
        """Move to the next token."""
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None

    def parse(self) -> ASTNode:
        """
        Parse the token list into an AST.

        Returns:
            The root node of the AST.

        Raises:
            MalformedExpressionError: If the expression is invalid.
        """
        if not self.tokens or (
            len(self.tokens) == 1 and self.tokens[0].type == TokenType.EOF
        ):
            raise MalformedExpressionError("Empty expression")

        result = self.expression()

        # Ensure we've consumed all tokens (except EOF)
        if self.current_token and self.current_token.type != TokenType.EOF:
            raise MalformedExpressionError(f"Unexpected token: {self.current_token}")

        return result

    def expression(self) -> ASTNode:
        """
        Parse an expression (handles + and -).

        expression := term ((PLUS | MINUS) term)*
        """
        node = self.term()

        while self.current_token is not None and self.current_token.type in (
            TokenType.PLUS,
            TokenType.MINUS,
        ):
            op = self.current_token.type
            self.advance()
            right = self.term()
            node = BinaryOpNode(left=node, operator=op, right=right)

        return node

    def term(self) -> ASTNode:
        """
        Parse a term (handles * and /).

        term := factor ((MULTIPLY | DIVIDE) factor)*
        """
        node = self.factor()

        while self.current_token is not None and self.current_token.type in (
            TokenType.MULTIPLY,
            TokenType.DIVIDE,
        ):
            op = self.current_token.type
            self.advance()
            right = self.factor()
            node = BinaryOpNode(left=node, operator=op, right=right)

        return node

    def factor(self) -> ASTNode:
        """
        Parse a factor (handles numbers and unary minus).

        factor := NUMBER | MINUS factor
        """
        token = self.current_token

        if token is None:
            raise MalformedExpressionError("Unexpected end of expression")

        if token.type == TokenType.NUMBER:
            self.advance()
            return NumberNode(value=token.value)  # type: ignore

        if token.type == TokenType.MINUS:
            self.advance()
            operand = self.factor()
            return UnaryOpNode(operator=TokenType.MINUS, operand=operand)

        raise MalformedExpressionError(f"Unexpected token: {token}")


# =============================================================================
# Evaluator (T047-T052)
# =============================================================================


class Evaluator:
    """
    Evaluates an AST and returns the result.

    The evaluator handles:
    - Number nodes: returns the value
    - Binary operations: +, -, *, /
    - Unary minus: negates the operand
    - Division: uses int() for truncation toward zero

    Raises:
        DivisionByZeroError: If division by zero is attempted.
    """

    def evaluate(self, node: ASTNode) -> int:
        """
        Evaluate an AST node and return the result.

        Args:
            node: The AST node to evaluate.

        Returns:
            The integer result of the evaluation.

        Raises:
            DivisionByZeroError: If division by zero is attempted.
        """
        if isinstance(node, NumberNode):
            return node.value

        if isinstance(node, UnaryOpNode):
            operand = self.evaluate(node.operand)
            if node.operator == TokenType.MINUS:
                return -operand
            raise InvalidOperatorError(f"Unknown unary operator: {node.operator}")

        if isinstance(node, BinaryOpNode):
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)

            if node.operator == TokenType.PLUS:
                return left + right
            if node.operator == TokenType.MINUS:
                return left - right
            if node.operator == TokenType.MULTIPLY:
                return left * right
            if node.operator == TokenType.DIVIDE:
                if right == 0:
                    raise DivisionByZeroError("Division by zero is not allowed")
                # Use int() for truncation toward zero (not // which floors)
                return int(left / right)

            raise InvalidOperatorError(f"Unknown operator: {node.operator}")

        raise MalformedExpressionError(f"Unknown node type: {type(node)}")


# =============================================================================
# Error Messages (T060-T061)
# =============================================================================

ERROR_MESSAGES: dict[type[CalculatorError], str] = {
    DivisionByZeroError: "Error: Division by zero is not allowed",
    InvalidOperandError: "Error: Invalid operand",
    InvalidOperatorError: "Error: Invalid operator",
    MalformedExpressionError: "Error: Malformed expression",
}


def get_error_message(error: CalculatorError) -> str:
    """
    Get a user-friendly error message for an exception.

    Args:
        error: The calculator error.

    Returns:
        A user-friendly error message string.
    """
    error_type = type(error)
    if error_type in ERROR_MESSAGES:
        return ERROR_MESSAGES[error_type]
    return f"Error: {str(error)}"


# =============================================================================
# CLI Interface (T068-T072)
# =============================================================================


def calculate(expression: str) -> int:
    """
    Calculate the result of a mathematical expression.

    Args:
        expression: The mathematical expression to evaluate.

    Returns:
        The integer result.

    Raises:
        CalculatorError: If the expression is invalid.
    """
    tokenizer = Tokenizer(expression)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    evaluator = Evaluator()
    return evaluator.evaluate(ast)


def main() -> None:
    """
    Main entry point for the CLI calculator.

    Usage:
        python calculator.py "<expression>"

    Exit codes:
        0: Success
        1: Error
    """
    import sys

    # Check for expression argument
    if len(sys.argv) < 2:
        print("Error: No expression provided", file=sys.stderr)
        print('Usage: python calculator.py "<expression>"', file=sys.stderr)
        sys.exit(1)

    expression = sys.argv[1]

    # Check for empty or whitespace-only input
    if not expression or expression.strip() == "":
        print("Error: Expression cannot be empty", file=sys.stderr)
        sys.exit(1)

    try:
        result = calculate(expression)
        print(result)
        sys.exit(0)
    except CalculatorError as e:
        print(get_error_message(e), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
