1. Programming Language & Environment
    a. Python-only implementation
    b. Latest stable Python version supported
    c. Command-line (CLI) based execution

2. Coding Standards & Project Structure
    a. Strict adherence to PEP 8
    b. Mandatory use of type hints (typing)
    c. Single-file implementation (calculator.py)
    d. Simple inline comments; no formal docstrings

3. Functional Scope
    a. Supported operations: Addition, Subtraction, Multiplication, Division
    b. Integer-only input and calculations

4. Edge Cases & Error Handling
    a. Division by zero must raise an explicit error
    b. Invalid input must be rejected with a clear error message

5. Package Management
    a. Use uv as the package manager

6. Mathematical Rules
    a. Automatic operator precedence using BODMAS

7. Testing & Validation
    a. Unit testing is mandatory
    b. Use pytest for test implementation
    
8. Features Development Strategy
    a. Build One feature at a time
    b. Each feature must be 
        - Fully specified
        - Implemented
        - Tested
        - Reviewed
        - before moving to the next feature