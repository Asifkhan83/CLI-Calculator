# Quickstart: Modulo Operator Implementation

**Feature**: 002-modulo-operator
**Estimated Time**: 30-45 minutes (TDD approach)

## Prerequisites

- Python 3.12+ installed
- uv package manager installed
- Repository cloned and on branch `002-modulo-operator`

## Setup

```bash
# Ensure you're on the correct branch
git checkout 002-modulo-operator

# Install dependencies
uv sync
```

## Implementation Steps

### Step 1: Write Failing Tests (RED Phase) - 15 min

Create `tests/test_modulo.py`:

```python
import pytest
from calculator import calculate, ModuloByZeroError

class TestBasicModulo:
    def test_simple_modulo(self):
        assert calculate("10 % 3") == 1
        
    def test_evenly_divisible(self):
        assert calculate("15 % 5") == 0
        
    def test_larger_divisor(self):
        assert calculate("3 % 10") == 3

class TestModuloPrecedence:
    def test_modulo_before_addition(self):
        assert calculate("10 + 7 % 3") == 11
        
    def test_modulo_with_multiplication(self):
        assert calculate("2 * 10 % 3") == 2

class TestModuloByZero:
    def test_modulo_by_zero_raises_error(self):
        with pytest.raises(ModuloByZeroError):
            calculate("10 % 0")
```

Run tests to verify they fail:
```bash
uv run pytest tests/test_modulo.py -v
```

### Step 2: Implement Modulo (GREEN Phase) - 10 min

Edit `calculator.py`:

1. Add exception class after `DivisionByZeroError`:
```python
class ModuloByZeroError(CalculatorError):
    """Raised when attempting modulo by zero."""
    pass
```

2. Update `TOKEN_PATTERN` in Tokenizer:
```python
TOKEN_PATTERN = re.compile(r'\s*(\d+|[+\-*/%()])\s*')
```

3. Update `_parse_term()` in Parser:
```python
while self.tokenizer.peek() in ('*', '/', '%'):
    # ... existing code ...
    else:  # operator == '%'
        if right == 0:
            raise ModuloByZeroError("Modulo by zero is not allowed")
        left = left % right
```

4. Update `main()` exception handling:
```python
except ModuloByZeroError as e:
    print(f"Error: {e}")
```

Run tests to verify they pass:
```bash
uv run pytest tests/test_modulo.py -v
```

### Step 3: Refactor and Validate (REFACTOR Phase) - 10 min

```bash
# Format code
uv run black calculator.py tests/

# Type check
uv run mypy calculator.py --strict

# Full test suite with coverage
uv run pytest --cov=calculator --cov-report=term-missing

# Verify all tests pass
uv run pytest -v
```

## Verification Checklist

- [ ] `10 % 3` returns `1`
- [ ] `10 + 7 % 3` returns `11` (precedence)
- [ ] `10 % 0` raises `ModuloByZeroError`
- [ ] All existing tests still pass
- [ ] Coverage >= 80%
- [ ] mypy: 0 errors
- [ ] black: 0 differences

## Commit

```bash
git add -A
git commit -m "feat(calc): add modulo operator with BODMAS precedence"
git push -u origin 002-modulo-operator
```
