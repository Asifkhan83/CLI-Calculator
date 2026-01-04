<!--
Sync Impact Report
==================
Version change: 1.0.0 → 1.1.0 (MINOR - Added governance and process sections)
Modified principles: None
Added sections:
  - Documentation Structure (.specify/ directory formalization)
  - CI/CD Guardrails (automated quality checks)
  - Git Branch Strategy (feature development flow)
  - ADR Process (under Governance)
  - Clarification Phase (in Development Workflow)
Removed sections: None
Templates requiring updates:
  - .specify/templates/plan-template.md ✅ (Compatible)
  - .specify/templates/spec-template.md ✅ (Compatible)
  - .specify/templates/tasks-template.md ✅ (Compatible)
Follow-up TODOs:
  - Create .specify/adr/ directory
  - Create .specify/specs/ directory structure
  - Setup CI/CD pipeline with pytest, mypy, black
-->

# Python Calculator Constitution

## Core Principles

### I. Python-Only CLI Implementation

- All code MUST be written in Python using the latest stable version
- Execution MUST be command-line (CLI) based only
- Implementation MUST be contained in a single file: `calculator.py`
- No GUI, web interface, or external service integrations permitted

**Rationale**: Single-file CLI keeps the project simple, portable, and easy to test.

### II. Code Quality Standards

- All code MUST strictly adhere to PEP 8 style guidelines
- Documentation MUST use simple inline comments only; no formal docstrings required
- Code MUST be readable and self-documenting

**Rationale**: Consistent style improves maintainability and readability.

### III. Type Safety

- Type hints (typing module) MUST be used for all function parameters and return types
- All variables with non-obvious types MUST have type annotations
- Static type checking SHOULD be used to verify type correctness
- No use of `Any` type unless absolutely necessary and justified

**Rationale**: Strong typing catches errors at development time and serves as documentation.

### IV. Integer Arithmetic Only

- All input values MUST be integers
- All calculation results MUST be integers
- Supported operations: Addition (+), Subtraction (-), Multiplication (*), Division (/)
- Operator precedence MUST follow BODMAS rules automatically

**Rationale**: Integer-only scope simplifies implementation while covering core arithmetic needs.

### V. Error Handling

- Division by zero MUST raise an explicit, descriptive error
- Invalid input (non-integer, malformed expressions) MUST be rejected with clear error messages
- Errors MUST be user-friendly and indicate the nature of the problem
- The program MUST NOT crash silently or produce undefined behavior

**Rationale**: Robust error handling ensures predictable behavior and good user experience.

### VI. Test-First Development

- Unit testing is MANDATORY for all features
- pytest MUST be used as the testing framework
- Tests MUST be written before implementation (Red-Green-Refactor cycle)
- All tests MUST pass before a feature is considered complete

**Rationale**: TDD ensures correctness and prevents regressions as features are added.

### VII. Simplicity & Minimal Dependencies

- Prefer Python standard library over external packages
- External dependencies MUST be justified and documented
- Code MUST favor simplicity over cleverness
- YAGNI (You Aren't Gonna Need It) principle MUST be followed
- No premature optimization or over-engineering

**Rationale**: Minimal dependencies reduce complexity, security risks, and maintenance burden.

### VIII. Feature Development Strategy

- Features MUST be built one at a time in sequence
- Each feature MUST complete the full cycle before starting the next:
  1. Fully specified (spec.md)
  2. Clarified (clarifications.md)
  3. Planned (plan.md)
  4. Implemented (code)
  5. Tested (pytest passing)
  6. Reviewed (quality verified)
  7. Committed to GitHub
- No parallel feature development; focused incremental delivery only
- Each completed feature MUST be committed to GitHub before moving to the next

**Rationale**: Sequential feature development with immediate commits ensures quality, traceability, and prevents incomplete work.

## Documentation Structure

The `.specify/` directory MUST follow this standardized structure:

```
.specify/
├── memory/
│   └── constitution.md          # This file - project principles
├── adr/
│   ├── ADR-001-*.md             # Architecture Decision Records
│   └── ADR-002-*.md
├── specs/
│   └── 001-feature-name/
│       ├── spec.md              # What: requirements & acceptance criteria
│       ├── plan.md              # How: technical approach & stack
│       ├── tasks.md             # Actionable implementation items
│       └── clarifications.md    # Q&A from specification phase
├── templates/                   # Reusable document templates
└── scripts/                     # Automation scripts
```

**Directory Requirements**:
- `memory/` - Constitution and persistent project context
- `adr/` - All Architecture Decision Records with sequential numbering
- `specs/` - Feature specifications with sequential prefix (001-, 002-, etc.)
- Each feature folder MUST contain spec.md at minimum
- Additional artifacts (plan.md, tasks.md, clarifications.md) added as workflow progresses

## Technical Standards

- **Package Manager**: uv MUST be used for all dependency management
- **Python Version**: Latest stable Python version supported
- **Project Structure**: Single-file implementation (`calculator.py`) at repository root
- **Test Location**: Tests in `tests/` directory using pytest conventions
- **Dependencies**: Minimize external dependencies; standard library preferred
- **Version Control**: Git with GitHub for remote repository

## CI/CD Guardrails

All code changes MUST pass automated checks before merge:

### Required Checks

| Tool | Purpose | Threshold |
|------|---------|-----------|
| pytest | Unit tests | 100% pass, minimum 80% coverage |
| mypy | Static type checking | 0 errors (strict mode) |
| black | Code formatting | 0 differences |

### Pipeline Configuration

- CI pipeline MUST run on all pull requests
- Pipeline failure MUST block merge to protected branches
- Coverage reports MUST be generated and tracked

### Branch Protection Rules (main)

- Require pull request before merging
- Require status checks to pass (pytest, mypy, black)
- Require at least 1 approval (if team > 1)
- No direct pushes to main allowed

## Git Branch Strategy

### Branch Structure

```
main              # Production-ready code only
└── develop       # Integration branch for features
    └── feature/  # Individual feature branches
```

### Branch Naming Convention

- Feature branches: `feature/<issue-number>-<short-description>`
- Example: `feature/001-basic-addition`

### Workflow

1. Create feature branch from `develop`
2. Implement feature following Development Workflow
3. Open PR to `develop` with constitution checklist
4. Pass all CI checks
5. Obtain approval and merge to `develop`
6. When release-ready, merge `develop` to `main`

### Pull Request Template Checklist

```markdown
## Constitution Compliance
- [ ] PEP 8 compliant (black formatted)
- [ ] Type hints on all functions (mypy passing)
- [ ] Tests written first (TDD)
- [ ] All tests passing (pytest)
- [ ] Minimal dependencies used
- [ ] Error handling implemented
- [ ] Single-file constraint maintained
- [ ] ADR created for architectural decisions (if applicable)
```

## Development Workflow

1. **Specification Phase**: Create feature spec with acceptance criteria in `specs/<feature>/spec.md`
2. **Clarification Phase**: Surface ambiguities using structured questioning; document all Q&A in `specs/<feature>/clarifications.md`; require sign-off before proceeding
3. **Planning Phase**: Define technical approach in `specs/<feature>/plan.md`
4. **Task Generation Phase**: Create actionable items in `specs/<feature>/tasks.md`
5. **Test Phase**: Write failing tests that define expected behavior (RED)
6. **Implementation Phase**: Write minimal code to make tests pass (GREEN)
7. **Refactor Phase**: Clean up code while keeping tests green (REFACTOR)
8. **Review Phase**: Verify code quality, PEP 8 compliance, type hints
9. **Commit Phase**: Commit completed feature to GitHub via PR
10. **Completion**: Feature merged only when all criteria met and pushed to remote

### Clarification Phase Requirements

- Use structured questioning to identify ambiguities in spec
- Questions MUST cover: edge cases, error scenarios, performance expectations
- All clarifications MUST be documented in `clarifications.md`
- Sign-off (explicit user approval) REQUIRED before proceeding to planning
- Format for clarifications:

```markdown
## Clarification Log

### Q1: [Question about ambiguous requirement]
**Asked**: YYYY-MM-DD
**Answer**: [User response]
**Impact**: [How this affects spec/implementation]

### Q2: ...
```

## Governance

- This Constitution supersedes all other development practices for this project
- Amendments require:
  - Documented rationale for the change
  - Review of impact on existing features
  - Version increment following semantic versioning
- All code reviews MUST verify compliance with these principles
- Deviations from the Constitution MUST be documented and justified in an ADR

### ADR Process

Architecture Decision Records MUST be created for significant technical decisions.

**When to Create an ADR**:
- Choosing between multiple viable technical approaches
- Decisions with long-term consequences (framework, data model, API design)
- Cross-cutting concerns affecting system architecture
- Security or performance-critical choices

**ADR Format**:

```markdown
# ADR-<NNN>: <Title>

**Status**: Proposed | Accepted | Deprecated | Superseded
**Date**: YYYY-MM-DD
**Decision Makers**: [names]

## Context
[What is the issue that we're seeing that motivates this decision?]

## Decision
[What is the change that we're proposing and/or doing?]

## Rationale
[Why is this the best choice among alternatives considered?]

## Alternatives Considered
1. [Alternative 1] - [Why rejected]
2. [Alternative 2] - [Why rejected]

## Consequences
### Positive
- [Benefit 1]
- [Benefit 2]

### Negative
- [Tradeoff 1]
- [Tradeoff 2]

## References
- [Git commit]: [link]
- [Related ADR]: [link]
```

**ADR Directory**: `.specify/adr/`
**Naming Convention**: `ADR-<NNN>-<short-description>.md`
**Linking Strategy**: Reference git commits that implement the decision
**Review Requirement**: ADR MUST be reviewed and accepted BEFORE implementation begins

**Version**: 1.1.0 | **Ratified**: 2026-01-04 | **Last Amended**: 2026-01-04
