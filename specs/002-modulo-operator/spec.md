# Feature Specification: Modulo Operator

**Feature Branch**: `002-modulo-operator`
**Created**: 2026-01-06
**Status**: Draft
**Input**: User description: "Modulo Operator - Add the modulo (%) operator to the CLI Calculator for computing remainders. The operator should follow BODMAS precedence (same level as multiplication/division), support integer-only arithmetic, handle division by zero for modulo, and integrate with existing expression parsing."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Basic Modulo Calculation (Priority: P1)

As a user, I want to calculate the remainder of integer division using the modulo operator (%), so that I can perform remainder-based calculations.

**Why this priority**: This is the core functionality of the feature. Without basic modulo calculation working, the feature has no value. This enables all common use cases like checking even/odd numbers, cycling through values, etc.

**Independent Test**: Can be fully tested by running `calculator "10 % 3"` and verifying the output is `1`. Delivers immediate value for remainder calculations.

**Acceptance Scenarios**:

1. **Given** the calculator is running, **When** I enter `10 % 3`, **Then** the output is `1` (10 divided by 3 leaves remainder 1)
2. **Given** the calculator is running, **When** I enter `15 % 5`, **Then** the output is `0` (15 is evenly divisible by 5)
3. **Given** the calculator is running, **When** I enter `7 % 4`, **Then** the output is `3` (7 divided by 4 leaves remainder 3)
4. **Given** the calculator is running, **When** I enter `100 % 7`, **Then** the output is `2`

---

### User Story 2 - Modulo with BODMAS Precedence (Priority: P2)

As a user, I want the modulo operator to follow BODMAS rules (same precedence as multiplication and division), so that complex expressions evaluate correctly.

**Why this priority**: Critical for mathematical correctness. Users expect standard operator precedence. Without this, expressions would produce incorrect results.

**Independent Test**: Can be tested by running `calculator "10 + 7 % 3"` and verifying the output is `11` (not `0`), demonstrating that modulo is evaluated before addition.

**Acceptance Scenarios**:

1. **Given** the calculator is running, **When** I enter `10 + 7 % 3`, **Then** the output is `11` (7 % 3 = 1, then 10 + 1 = 11)
2. **Given** the calculator is running, **When** I enter `20 - 10 % 3`, **Then** the output is `19` (10 % 3 = 1, then 20 - 1 = 19)
3. **Given** the calculator is running, **When** I enter `2 * 10 % 3`, **Then** the output is `2` (left-to-right: 2 * 10 = 20, then 20 % 3 = 2)
4. **Given** the calculator is running, **When** I enter `10 % 3 * 2`, **Then** the output is `2` (left-to-right: 10 % 3 = 1, then 1 * 2 = 2)
5. **Given** the calculator is running, **When** I enter `15 / 3 % 2`, **Then** the output is `1` (left-to-right: 15 / 3 = 5, then 5 % 2 = 1)

---

### User Story 3 - Modulo by Zero Error Handling (Priority: P3)

As a user, I want to receive a clear error message when attempting modulo by zero, so that I understand why the calculation failed.

**Why this priority**: Essential for robustness and user experience. While not the core feature, users need clear feedback when they make invalid requests.

**Independent Test**: Can be tested by running `calculator "10 % 0"` and verifying an error message is displayed to stderr with exit code 1.

**Acceptance Scenarios**:

1. **Given** the calculator is running, **When** I enter `10 % 0`, **Then** an error message is displayed indicating modulo by zero is not allowed, and exit code is 1
2. **Given** the calculator is running, **When** I enter `5 + 10 % 0`, **Then** an error message is displayed, and exit code is 1

---

### User Story 4 - Modulo with Negative Numbers (Priority: P4)

As a user, I want to use the modulo operator with negative integers, so that I can perform remainder calculations with negative values.

**Why this priority**: Lower priority as negative modulo is less commonly needed, but necessary for complete integer arithmetic support.

**Independent Test**: Can be tested by running `calculator "-10 % 3"` and verifying correct mathematical behavior.

**Acceptance Scenarios**:

1. **Given** the calculator is running, **When** I enter `-10 % 3`, **Then** the output follows Python's modulo semantics (result has same sign as divisor)
2. **Given** the calculator is running, **When** I enter `10 % -3`, **Then** the output follows Python's modulo semantics
3. **Given** the calculator is running, **When** I enter `-10 % -3`, **Then** the output follows Python's modulo semantics

---

### Edge Cases

- What happens when the dividend is smaller than the divisor? (e.g., `3 % 10` should return `3`)
- What happens with modulo by 1? (e.g., `10 % 1` should return `0`)
- What happens with chained modulo operations? (e.g., `100 % 7 % 3` should evaluate left-to-right)
- What happens when modulo is used with parentheses? (e.g., `(10 + 5) % 4` should return `3`)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST recognize `%` as a valid operator token during tokenization
- **FR-002**: System MUST parse `%` with the same precedence level as `*` and `/` (higher than `+` and `-`)
- **FR-003**: System MUST evaluate `%` left-to-right when at same precedence level as `*` or `/`
- **FR-004**: System MUST compute modulo using integer arithmetic (truncating toward zero for consistency with division)
- **FR-005**: System MUST raise a clear error when modulo by zero is attempted
- **FR-006**: System MUST support modulo with negative operands following Python semantics
- **FR-007**: System MUST support modulo within complex expressions containing other operators
- **FR-008**: System MUST support modulo with parenthesized sub-expressions

### Key Entities

- **Token**: Extended to include MODULO token type (`%`)
- **AST Node**: Binary operation node extended to handle modulo operator
- **Error Types**: Existing DivisionByZeroError repurposed or new ModuloByZeroError for modulo-specific errors

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All basic modulo operations (`a % b`) return correct remainder for positive integers
- **SC-002**: Modulo operator follows BODMAS precedence (evaluated at same level as `*` and `/`)
- **SC-003**: Modulo by zero displays a clear error message to stderr and exits with code 1
- **SC-004**: Complex expressions mixing `%` with other operators evaluate correctly
- **SC-005**: All existing calculator functionality continues to work without regression
- **SC-006**: Test coverage for modulo functionality is at least 80%

## Assumptions

- The `%` symbol is not currently used for any other purpose in the calculator
- Python's modulo semantics (result has same sign as divisor) are acceptable for negative number handling
- The existing tokenizer, parser, and evaluator architecture can be extended to support the new operator
- Error handling for modulo by zero can follow the same pattern as division by zero

## Out of Scope

- Floating-point modulo operations
- Modulo assignment operator (`%=`)
- Alternative modulo syntax (e.g., `mod` keyword)
- Configurable modulo semantics (truncated vs floored)

## Dependencies

- Existing CLI Calculator implementation (tokenizer, parser, evaluator)
- pytest testing framework
- mypy for type checking
