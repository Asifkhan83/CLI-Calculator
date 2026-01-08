"""CLI Calculator with BODMAS precedence support."""

import re
import sys
from typing import Union


class CalculatorError(Exception):
    """Base exception for calculator errors."""

    pass


class DivisionByZeroError(CalculatorError):
    """Raised when attempting to divide by zero."""

    pass


class ModuloByZeroError(CalculatorError):
    """Raised when attempting modulo by zero."""

    pass


class InvalidInputError(CalculatorError):
    """Raised when input is invalid."""

    pass


class Tokenizer:
    """Tokenizes mathematical expressions into operators and numbers."""

    TOKEN_PATTERN = re.compile(r"\s*(\d+|[+\-*/()])\s*")

    def __init__(self, expression: str) -> None:
        self.expression = expression
        self.tokens: list[str] = []
        self.position = 0
        self._tokenize()

    def _tokenize(self) -> None:
        """Convert expression string into list of tokens."""
        pos = 0
        while pos < len(self.expression):
            match = self.TOKEN_PATTERN.match(self.expression, pos)
            if match:
                token = match.group(1)
                self.tokens.append(token)
                pos = match.end()
            else:
                invalid_char = self.expression[pos]
                raise InvalidInputError(f"Invalid character: '{invalid_char}'")

    def peek(self) -> Union[str, None]:
        """Look at current token without consuming it."""
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None

    def consume(self) -> Union[str, None]:
        """Consume and return current token."""
        token = self.peek()
        if token is not None:
            self.position += 1
        return token


class Parser:
    """Recursive descent parser for mathematical expressions with BODMAS."""

    def __init__(self, tokenizer: Tokenizer) -> None:
        self.tokenizer = tokenizer

    def parse(self) -> int:
        """Parse and evaluate the expression."""
        result = self._parse_expression()
        if self.tokenizer.peek() is not None:
            raise InvalidInputError(f"Unexpected token: '{self.tokenizer.peek()}'")
        return result

    def _parse_expression(self) -> int:
        """Parse addition and subtraction (lowest precedence)."""
        left = self._parse_term()

        while self.tokenizer.peek() in ("+", "-"):
            operator = self.tokenizer.consume()
            right = self._parse_term()
            if operator == "+":
                left = left + right
            else:
                left = left - right

        return left

    def _parse_term(self) -> int:
        """Parse multiplication and division (higher precedence)."""
        left = self._parse_factor()

        while self.tokenizer.peek() in ("*", "/"):
            operator = self.tokenizer.consume()
            right = self._parse_factor()
            if operator == "*":
                left = left * right
            else:
                if right == 0:
                    raise DivisionByZeroError("Division by zero is not allowed")
                left = left // right

        return left

    def _parse_factor(self) -> int:
        """Parse numbers and parenthesized expressions (highest precedence)."""
        token = self.tokenizer.peek()

        if token is None:
            raise InvalidInputError("Unexpected end of expression")

        # Handle negative numbers at the start or after operator
        if token == "-":
            self.tokenizer.consume()
            return -self._parse_factor()

        if token == "+":
            self.tokenizer.consume()
            return self._parse_factor()

        if token == "(":
            self.tokenizer.consume()
            result = self._parse_expression()
            if self.tokenizer.consume() != ")":
                raise InvalidInputError("Missing closing parenthesis")
            return result

        if token.isdigit() or (token[0].isdigit() if token else False):
            self.tokenizer.consume()
            return int(token)

        raise InvalidInputError(f"Unexpected token: '{token}'")


def calculate(expression: str) -> int:
    """
    Calculate the result of a mathematical expression.

    Supports +, -, *, / operators with BODMAS precedence.
    Only integer arithmetic is supported.
    """
    if not expression or not expression.strip():
        raise InvalidInputError("Empty expression")

    tokenizer = Tokenizer(expression)
    parser = Parser(tokenizer)
    return parser.parse()


def main() -> None:
    """Main entry point for CLI calculator."""
    print("CLI Calculator")
    print("Supported operations: +, -, *, / with BODMAS precedence")
    print("Enter 'quit' or 'exit' to stop")
    print("-" * 40)

    while True:
        try:
            expression = input("\nEnter expression: ").strip()

            if expression.lower() in ("quit", "exit", "q"):
                print("Goodbye!")
                break

            if not expression:
                continue

            result = calculate(expression)
            print(f"Result: {result}")

        except DivisionByZeroError as e:
            print(f"Error: {e}")
        except InvalidInputError as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except EOFError:
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()
