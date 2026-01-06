# CLI Calculator

A command-line calculator supporting integer arithmetic with BODMAS operator precedence.

## Features

- Basic arithmetic operations: `+`, `-`, `*`, `/`
- BODMAS operator precedence (multiplication/division before addition/subtraction)
- Left-to-right associativity for same-precedence operators
- Unary minus support (at expression start and after operators)
- Integer division with truncation toward zero
- Comprehensive error handling

## Installation

Requires Python 3.11+ and [uv](https://github.com/astral-sh/uv) package manager.

```bash
# Clone the repository
git clone https://github.com/Asifkhan83/CLI-Calculator.git
cd CLI-Calculator

# Install dependencies
uv sync --dev
```

## Usage

```bash
python calculator.py "<expression>"
```

### Examples

```bash
# Basic arithmetic
python calculator.py "5 + 3"        # 8
python calculator.py "10 - 4"       # 6
python calculator.py "6 * 7"        # 42
python calculator.py "20 / 4"       # 5

# BODMAS precedence
python calculator.py "2 + 3 * 4"    # 14 (not 20)
python calculator.py "10 - 6 / 2"   # 7 (not 2)

# Integer division (truncates toward zero)
python calculator.py "15 / 2"       # 7
python calculator.py "-7 / 2"       # -3 (not -4)

# Negative numbers
python calculator.py "-5 + 3"       # -2
python calculator.py "5 - -3"       # 8
python calculator.py "5 * -3"       # -15

# Chained operations (left-to-right)
python calculator.py "10 - 5 - 2"   # 3
python calculator.py "100 / 10 / 2" # 5
```

### Exit Codes

- `0` - Success (result printed to stdout)
- `1` - Error (message printed to stderr)

### Error Handling

```bash
python calculator.py "10 / 0"       # Error: Division by zero is not allowed
python calculator.py "5 + abc"      # Error: Invalid operand
python calculator.py "5 @ 3"        # Error: Invalid operand
python calculator.py ""             # Error: Expression cannot be empty
python calculator.py "5 +"          # Error: Malformed expression
```

## Development

### Running Tests

```bash
# Run all tests
uv run pytest tests/ -v

# Run with coverage
uv run pytest --cov=calculator --cov-report=term-missing

# Run specific test file
uv run pytest tests/test_tokenizer.py -v
```

### Code Quality

```bash
# Type checking (strict mode)
uv run mypy calculator.py --strict

# Code formatting
uv run black calculator.py tests/
```

### Test Coverage

The project maintains 80%+ test coverage with 148 tests across:

- `test_tokenizer.py` - Tokenization tests
- `test_parser.py` - Parser and AST tests
- `test_evaluator.py` - Evaluation and arithmetic tests
- `test_cli.py` - CLI interface tests
- `test_edge_cases.py` - Edge cases and acceptance scenarios

## Architecture

Single-file implementation using a recursive descent parser:

1. **Tokenizer** - Converts expression string to tokens
2. **Parser** - Builds Abstract Syntax Tree (AST) with BODMAS precedence
3. **Evaluator** - Walks AST and computes result
4. **CLI** - Handles command-line interface and error reporting

### Grammar (EBNF)

```
expression := term ((PLUS | MINUS) term)*
term       := factor ((MULTIPLY | DIVIDE) factor)*
factor     := NUMBER | MINUS factor
```

## Project Principles

1. **Python-only implementation** - Single-file `calculator.py`
2. **PEP 8 compliant** - Strict adherence to Python style guide
3. **Type hints** - Full type annotations throughout
4. **BODMAS precedence** - Correct mathematical operator precedence
5. **TDD approach** - Tests written first, then implementation

## License

MIT
