# Feature Specification: CLI Calculator

**Feature Branch**: `001-cli-calculator`
**Created**: 2026-01-04
**Status**: Draft
**Input**: User description: "Build a basic CLI based calculator that handles addition, subtraction, multiplication and division"

## CLI Interface

### Invocation Syntax

The calculator accepts a mathematical expression as a command-line argument and returns the result.

**Usage Pattern**: `calculator "<expression>"`

**Examples**:
- `calculator "5 + 3"` → outputs `8`
- `calculator "2 + 3 * 4"` → outputs `14`
- `calculator "-5 + 10"` → outputs `5`

### Output Format

- **Success**: Displays the integer result on a single line to **stdout**
- **Error**: Displays an error message starting with `Error:` to **stderr**

### Exit Codes

| Exit Code | Meaning | When Used |
|-----------|---------|-----------|
| `0` | Success | Expression evaluated successfully |
| `1` | Error | Any error occurred (invalid input, division by zero, etc.) |

### Standard Streams

- **stdout**: Used ONLY for successful calculation results (integer value)
- **stderr**: Used ONLY for error messages (starting with `Error:`)
- No mixing of success/error output on the same stream

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Basic Arithmetic Calculation (Priority: P1)

As a user, I want to enter a mathematical expression containing integers and basic operators (+, -, *, /) so that I can quickly calculate results from the command line without needing a graphical calculator.

**Why this priority**: This is the core functionality - without the ability to perform calculations, the calculator has no value. This story enables all four arithmetic operations in a single implementation.

**Independent Test**: Can be fully tested by running the calculator with expressions like `2 + 3`, `10 - 4`, `6 * 7`, `20 / 5` and verifying correct integer results.

**Acceptance Scenarios**:

1. **Given** the calculator is ready to accept input, **When** the user enters `5 + 3`, **Then** the system displays `8`
2. **Given** the calculator is ready to accept input, **When** the user enters `10 - 4`, **Then** the system displays `6`
3. **Given** the calculator is ready to accept input, **When** the user enters `6 * 7`, **Then** the system displays `42`
4. **Given** the calculator is ready to accept input, **When** the user enters `20 / 4`, **Then** the system displays `5`
5. **Given** the calculator is ready to accept input, **When** the user enters `15 / 2`, **Then** the system displays `7` (integer division, truncated toward zero)
6. **Given** the calculator is ready to accept input, **When** the user enters `10 - 5 - 2`, **Then** the system displays `3` (left-to-right evaluation)
7. **Given** the calculator is ready to accept input, **When** the user enters `20 - 10 - 5 - 3`, **Then** the system displays `2` (chained subtraction)

---

### User Story 2 - BODMAS Operator Precedence (Priority: P2)

As a user, I want the calculator to automatically apply correct mathematical operator precedence (BODMAS: Brackets, Orders, Division, Multiplication, Addition, Subtraction) so that complex expressions are evaluated correctly without me needing to add parentheses.

**Why this priority**: Correct operator precedence is essential for mathematical accuracy. Without it, expressions like `2 + 3 * 4` would give wrong results, making the calculator unreliable.

**Independent Test**: Can be tested by entering expressions with multiple operators and verifying precedence is applied (e.g., `2 + 3 * 4` should return `14`, not `20`).

**Acceptance Scenarios**:

1. **Given** the calculator is ready, **When** the user enters `2 + 3 * 4`, **Then** the system displays `14` (multiplication before addition)
2. **Given** the calculator is ready, **When** the user enters `10 - 6 / 2`, **Then** the system displays `7` (division before subtraction)
3. **Given** the calculator is ready, **When** the user enters `2 * 3 + 4 * 5`, **Then** the system displays `26` (both multiplications before addition)
4. **Given** the calculator is ready, **When** the user enters `100 / 10 / 2`, **Then** the system displays `5` (left-to-right for same precedence)
5. **Given** the calculator is ready, **When** the user enters `20 / 4 / 2`, **Then** the system displays `2` (chained division, left-to-right)
6. **Given** the calculator is ready, **When** the user enters `10 - 3 - 2`, **Then** the system displays `5` (subtraction left-to-right, NOT 10 - (3-2) = 9)

---

### User Story 3 - Division by Zero Handling (Priority: P3)

As a user, I want to receive a clear error message when I attempt to divide by zero so that I understand why the calculation cannot be completed.

**Why this priority**: Error handling for division by zero is a critical edge case that must be handled gracefully to prevent crashes and provide user guidance.

**Independent Test**: Can be tested by entering expressions with zero divisors and verifying appropriate error messages are displayed.

**Acceptance Scenarios**:

1. **Given** the calculator is ready, **When** the user enters `10 / 0`, **Then** the system displays a clear error message to stderr and exits with code `1`
2. **Given** the calculator is ready, **When** the user enters `5 + 10 / 0`, **Then** the system displays a clear error message (division by zero detected during evaluation) and exits with code `1`

---

### User Story 4 - Invalid Input Handling (Priority: P4)

As a user, I want to receive a clear error message when I enter invalid input (non-integers, malformed expressions, unsupported characters) so that I understand what input format is expected.

**Why this priority**: Robust input validation ensures the calculator doesn't crash on unexpected input and guides users toward correct usage.

**Independent Test**: Can be tested by entering various invalid inputs and verifying appropriate error messages are displayed.

**Acceptance Scenarios**:

1. **Given** the calculator is ready, **When** the user enters `abc`, **Then** the system displays an error message to stderr and exits with code `1`
2. **Given** the calculator is ready, **When** the user enters `3.14 + 2`, **Then** the system displays an error message indicating only integers are supported
3. **Given** the calculator is ready, **When** the user enters `5 +`, **Then** the system displays an error message indicating incomplete expression
4. **Given** the calculator is ready, **When** the user enters `5 ^ 2`, **Then** the system displays an error message indicating unsupported operator
5. **Given** the calculator is ready, **When** the user enters an empty string `""`, **Then** the system displays an error message indicating input is required
6. **Given** the calculator is ready, **When** the user enters whitespace only `"   "`, **Then** the system displays an error message indicating input is required
7. **Given** the calculator is ready, **When** no argument is provided, **Then** the system displays an error message indicating input is required

---

### Edge Cases

- What happens when the user enters very large integers that exceed typical bounds? (Assumption: System handles within standard integer limits)
- What happens when the user enters negative numbers? (Defined: Supported in both unary and binary positions)
- What happens when the user enters expressions with extra whitespace? (Defined: Whitespace is trimmed/ignored)
- What happens when division result is not a whole number? (Defined: Integer division truncates toward zero)
- What happens with empty or whitespace-only input? (Defined: Error with clear message)

## Input Format Specification

### Valid Input Examples

| Input | Description | Expected Output |
|-------|-------------|-----------------|
| `5 + 3` | With spaces | `8` |
| `5+3` | Without spaces | `8` |
| `-5 + 3` | Unary minus at expression start | `-2` |
| `5 + -3` | Unary minus after operator | `2` |
| `5 * -3` | Unary minus in multiplication | `-15` |
| `10 / -2` | Negative divisor | `-5` |
| `-10 / -2` | Both operands negative | `5` |
| `2 + 3 * 4 - 1` | Multiple operators | `13` |
| `100 / 10 / 2` | Chained division | `5` |
| `10 - 5 - 2` | Chained subtraction | `3` |
| `20 - 10 - 5 - 3` | Multiple chained subtraction | `2` |

### Integer Division with Negative Operands

Integer division MUST truncate toward zero (not floor toward negative infinity):

| Expression | Result | Explanation |
|------------|--------|-------------|
| `7 / 2` | `3` | Positive result, truncated |
| `-7 / 2` | `-3` | NOT `-4`; truncates toward zero |
| `7 / -2` | `-3` | NOT `-4`; truncates toward zero |
| `-7 / -2` | `3` | Positive result, truncated |

### Unary Minus Operator

The minus sign (`-`) can be used in two contexts:

1. **Unary minus** (negation): Applies to a single operand
   - At expression start: `-5 + 3` → `-2`
   - After a binary operator: `5 + -3` → `2`, `5 * -3` → `-15`

2. **Binary minus** (subtraction): Between two operands
   - `5 - 3` → `2`

**Unary minus binding**: Unary minus binds tightly to its operand. Expression `-5 * 3` means `(-5) * 3 = -15`, NOT `-(5 * 3) = -15` (same result in this case, but conceptually different).

### Invalid Input Examples

| Input | Error Type | Why Invalid |
|-------|------------|-------------|
| `abc` | Invalid operand | Non-numeric characters |
| `3.14 + 2` | Invalid operand | Decimal numbers not supported |
| `5 +` | Malformed expression | Missing operand after operator |
| `+ 5` | Malformed expression | Plus cannot be unary (use `5` instead) |
| `5 ^ 2` | Invalid operator | Unsupported operator symbol |
| `5 / / 2` | Malformed expression | Consecutive operators |
| `""` (empty) | Empty input | No expression provided |
| `"   "` (whitespace) | Empty input | Only whitespace, no expression |
| `5 6 +` | Malformed expression | Invalid syntax |
| `--5` | Malformed expression | Double unary minus not supported |

### Input Rules

1. **Operands**: Must be integers (positive or negative, no decimals)
2. **Operators**: Only `+`, `-`, `*`, `/` are supported
3. **Whitespace**: Optional between tokens; ignored during evaluation
4. **Empty/Whitespace input**: Treated as error, must have at least one valid token
5. **Unary minus**: Supported at expression start and immediately after any binary operator
6. **Expression structure**: Must form valid mathematical expression with alternating operands and binary operators

## Error Handling Specification

### Error Message Types

| Error Type | Trigger Condition | Example Message | Exit Code |
|------------|-------------------|-----------------|-----------|
| Division by Zero | Right operand of `/` is `0` | `Error: Division by zero is not allowed` | `1` |
| Invalid Operand | Non-integer value (letters, decimals, symbols) | `Error: Invalid operand 'abc'. Only integers are allowed.` | `1` |
| Invalid Operator | Unsupported operator symbol | `Error: Unsupported operator '^'. Supported operators: +, -, *, /` | `1` |
| Malformed Expression | Incomplete or syntactically invalid | `Error: Incomplete expression. Expected operand after '+'.` | `1` |
| Empty Input | No expression or whitespace only | `Error: No input provided. Please enter a mathematical expression.` | `1` |
| No Argument | Calculator invoked without argument | `Error: No input provided. Usage: calculator "<expression>"` | `1` |

### Error Message Requirements

1. **Specificity**: Messages MUST indicate exactly what went wrong (not generic "invalid input")
2. **Guidance**: Messages SHOULD include what format is expected
3. **Clarity**: Messages MUST be understandable by non-technical users
4. **Consistency**: All error messages MUST start with `Error:`
5. **Stream**: All error messages MUST be written to stderr (not stdout)
6. **Exit Code**: All errors MUST result in exit code `1`

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST accept mathematical expressions as command-line input
- **FR-002**: System MUST support addition (+), subtraction (-), multiplication (*), and division (/) operations
- **FR-003**: System MUST accept only integer operands (whole numbers, positive or negative)
- **FR-004**: System MUST apply BODMAS operator precedence automatically
- **FR-005**: System MUST perform integer division truncating toward zero (NOT floor division)
- **FR-006**: System MUST display a clear error message when division by zero is attempted
- **FR-007**: System MUST display a clear error message when invalid input is provided
- **FR-008**: System MUST display the calculated result to stdout after successful evaluation
- **FR-009**: System MUST handle negative integers via unary minus at expression start and after operators
- **FR-010**: System MUST handle expressions with multiple operators (e.g., `2 + 3 * 4 - 1`)
- **FR-011**: System MUST accept expressions with or without spaces between operands and operators
- **FR-012**: Error messages MUST be specific, written to stderr, and include guidance on expected input format
- **FR-013**: System MUST evaluate same-precedence operators left-to-right (e.g., `10 - 5 - 2 = 3`)
- **FR-014**: System MUST exit with code `0` on success and code `1` on any error
- **FR-015**: System MUST treat empty input and whitespace-only input as errors

### Key Entities

- **Expression**: A mathematical expression string containing integers and operators (+, -, *, /)
- **Operand**: An integer value (positive or negative) within an expression
- **Operator**: A mathematical operation symbol (+, -, *, /)
- **Result**: The integer outcome of evaluating an expression

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can perform any basic arithmetic calculation (add, subtract, multiply, divide) in a single command execution
- **SC-002**: All calculations with multiple operators return mathematically correct results following BODMAS precedence and left-to-right associativity
- **SC-003**: 100% of division-by-zero attempts result in a clear, user-friendly error message to stderr (no crashes or unclear errors)
- **SC-004**: 100% of invalid input attempts result in a clear, user-friendly error message to stderr indicating the problem
- **SC-005**: Calculation completes and displays result immediately upon execution (no perceptible delay for typical expressions)
- **SC-006**: Error messages clearly indicate what went wrong and what input format is expected
- **SC-007**: Users can enter expressions with or without spaces and receive correct results
- **SC-008**: Exit codes accurately reflect success (0) or failure (1) for use in shell scripts and automation

## Assumptions

- Integer division truncates toward zero (e.g., `7 / 2 = 3`, `-7 / 2 = -3`, NOT `-4`)
- Whitespace in expressions is ignored/trimmed
- Empty and whitespace-only inputs are treated as errors
- Unary minus supported at start and after operators; unary plus is NOT supported
- Standard integer limits apply (no arbitrary precision)
- Single expression per execution (not a REPL/interactive mode)
- Parentheses/brackets are NOT supported in this initial version (BODMAS without the B and O)
- Same-precedence operators evaluate left-to-right (standard mathematical convention)
- Implementation language is Python as mandated by project constitution (not a spec concern)
