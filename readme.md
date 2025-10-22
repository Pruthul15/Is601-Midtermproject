# Advanced Calculator with Design Patterns - Midterm Project

[![Python application](https://github.com/Pruthul15/is601-Midtermproject/actions/workflows/python-app.yml/badge.svg)](https://github.com/Pruthul15/is601-Midtermproject/actions/workflows/python-app.yml)
[![Coverage](https://img.shields.io/badge/coverage-99%25-brightgreen.svg)](https://github.com/Pruthul15/is601-Midtermproject)

A professional command-line calculator application built with Python that implements multiple design patterns, comprehensive testing, and CI/CD automation.

**Author:** Pruthul Patel  
**Repository:** https://github.com/Pruthul15/is601-Midtermproject

---

## Features

**Core Operations:**
- Basic: add, subtract, multiply, divide
- Advanced: power, root, modulus, int_divide, percent, abs_diff

**Advanced Functionality:**
- Undo/redo using Memento pattern
- History management with pandas DataFrames
- Auto-save to CSV files using Observer pattern
- Color-coded output with Colorama
- Dynamic help menu with Decorator pattern
- Command pattern for operation encapsulation
- Configuration through environment variables
- Comprehensive error handling

**Quality Metrics:**
- 99% test coverage with 307 tests
- All tests passing with CI/CD automation
- 7 design patterns implemented

---

## Installation Instructions

### 1. Clone and Setup
```bash
git clone https://github.com/Pruthul15/is601-Midtermproject.git
cd is601-Midtermproject
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Create Configuration File
Create a `.env` file in the project root:

```env
CALCULATOR_MAX_HISTORY_SIZE=100
CALCULATOR_AUTO_SAVE=true
CALCULATOR_PRECISION=10
CALCULATOR_MAX_INPUT_VALUE=1e999
CALCULATOR_DEFAULT_ENCODING=utf-8
```

### 3. Run the Calculator
```bash
python main.py
```

---

## Usage Guide

### Available Commands

**Operations:** add, subtract, multiply, divide, power, root, modulus, int_divide, percent, abs_diff  
**History:** history, clear, save, load  
**State:** undo, redo  
**Utility:** help, exit

### Example Session

```
Enter command: add
First number: 15
Second number: 7
✓ SUCCESS: Result: 22

Enter command: power
First number: 2
Second number: 8
= RESULT: Result: 256

Enter command: history
=== Calculation History: ===
  1. Addition(15, 7) = 22
  2. Exponentiation(2, 8) = 256

Enter command: undo
✓ SUCCESS: Operation undone

Enter command: exit
✓ SUCCESS: History saved successfully. Goodbye!
```

---

## Project Structure

```
is601-Midtermproject/
├── .github/
│   └── workflows/
│       ├── python-app.yml          # Main CI/CD workflow
│       └── tests.yml               # Additional test workflow
├── app/
│   ├── __init__.py
│   ├── calculation.py              # Calculation data model
│   ├── calculator.py               # Main calculator (Facade pattern)
│   ├── calculator_config.py        # Configuration management
│   ├── calculator_memento.py       # Memento pattern for undo/redo
│   ├── calculator_repl.py          # REPL command-line interface
│   ├── colors.py                   # Colorama color output
│   ├── command_pattern.py          # Command pattern implementation
│   ├── exceptions.py               # Custom exception classes
│   ├── help_decorator.py           # Decorator pattern for help menu
│   ├── history.py                  # Observer pattern for history
│   ├── input_validators.py         # Input validation
│   └── operations.py               # Factory & Strategy patterns
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_calculation.py         # 29 tests
│   ├── test_calculator.py          # 36 tests
│   ├── test_calculator_memento.py  # 12 tests
│   ├── test_calculator_repl.py     # 31 tests
│   ├── test_colors.py              # 33 tests
│   ├── test_command_pattern.py     # 44 tests
│   ├── test_config.py              # 18 tests
│   ├── test_exceptions.py          # 7 tests
│   ├── test_help_decorator.py      # 38 tests
│   ├── test_history.py             # 7 tests
│   ├── test_operations.py          # 50 tests
│   └── test_validators.py          # 18 tests
├── history/                        # Auto-created for CSV files
├── logs/                           # Auto-created for log files
├── .env                            # Environment configuration
├── .gitignore
├── main.py                         # Application entry point
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

---

## Design Patterns

| Pattern | Purpose | Implementation |
|---------|---------|----------------|
| **Factory** | Create operation instances | `OperationFactory` in operations.py |
| **Memento** | Undo/redo functionality | `CalculatorMemento` for state management |
| **Observer** | Auto-save notifications | `LoggingObserver`, `AutoSaveObserver` |
| **Strategy** | Interchangeable operations | `Operation` base class |
| **Facade** | Simplified interface | `Calculator` class |
| **Command** | Request encapsulation | Command classes in command_pattern.py |
| **Decorator** | Dynamic help generation | `DynamicHelpGenerator` |

---

## Error Handling Examples

**Division by Zero:**
```
Enter command: divide
First number: 10
Second number: 0
✗ ERROR: Operation failed: Division by zero is not allowed
```

**Invalid Input:**
```
Enter command: add
First number: abc
✗ ERROR: Invalid number format: abc
```

**Root of Negative Number:**
```
Enter command: root
First number: -25
Second number: 2
✗ ERROR: Cannot calculate root of negative number
```

**Unknown Command:**
```
Enter command: xyz
✗ ERROR: Unknown command: 'xyz'. Type 'help' for available commands.
```

---

## Testing

### Run Tests
```bash
pytest                          # Run all tests
pytest -v                       # Verbose output
pytest --cov=app tests/         # With coverage report
pytest --cov=app --cov-fail-under=90 tests/  # Enforce 90% threshold
```

### Test Coverage
- **Total Tests:** 307
- **Coverage:** 99%
- **Status:** All tests passing

**Coverage by Module:**
```
app/calculator.py          100%
app/operations.py          100%
app/history.py             100%
app/exceptions.py          100%
app/calculator_config.py   100%
app/calculator_memento.py  100%
app/input_validators.py    100%
app/colors.py              100%
app/help_decorator.py      100%
app/calculator_repl.py      98%
app/command_pattern.py      99%
app/calculation.py          96%
```

---

## CI/CD with GitHub Actions

**Automated testing runs on every push:**
- Sets up Python 3.12 environment
- Installs dependencies from requirements.txt
- Runs full test suite with coverage
- Enforces 90% coverage threshold
- Fails if tests don't pass

**View Workflow:** `.github/workflows/python-app.yml`  
**Check Status:** [GitHub Actions](https://github.com/Pruthul15/is601-Midtermproject/actions)

---

## Data Management with pandas

**History Storage:**
- Stored in pandas DataFrame
- Auto-saves to CSV: `history/calculator_history.csv`
- Includes: operation, operands, result, timestamp
- Load/save functionality for persistence

**Example CSV:**
```csv
operation,operand1,operand2,result,timestamp
Addition,15,7,22,2025-10-09T20:18:12.165424
Exponentiation,2,8,256,2025-10-09T20:18:15.273261
```

---

## Configuration Options

Set in `.env` file:

| Variable | Description | Default |
|----------|-------------|---------|
| CALCULATOR_MAX_HISTORY_SIZE | Max history entries | 100 |
| CALCULATOR_AUTO_SAVE | Auto-save after operations | true |
| CALCULATOR_PRECISION | Decimal precision | 10 |
| CALCULATOR_MAX_INPUT_VALUE | Max input allowed | 1e999 |
| CALCULATOR_DEFAULT_ENCODING | File encoding | utf-8 |

---

## Optional Advanced Features

This project implements **3 optional features** (only 1 required for A):

### 1. Dynamic Help Menu (Decorator Pattern)
- Automatically generates help based on available operations
- Adding new operations updates help menu automatically
- Implementation: `app/help_decorator.py`

### 2. Color-Coded Output (Colorama)
- Enhanced readability with colored terminal output
- Green for success, red for errors, yellow for warnings
- Implementation: `app/colors.py`

### 3. Command Pattern
- Encapsulates requests as objects
- Enables operation queuing and logging
- Implementation: `app/command_pattern.py`

---

## Requirements

**Python Packages:**
```
Python 3.12+
pandas>=2.2.3
python-dotenv>=1.0.1
colorama>=0.4.6
pytest>=8.3.3
pytest-cov>=6.0.0
```

**Full list:** See `requirements.txt`

---

## Learning Outcomes Demonstrated

✅ **CLO1:** Git version control and collaborative development  
✅ **CLO2:** Linux command-line proficiency  
✅ **CLO3:** Python applications with automated testing  
✅ **CLO4:** CI/CD with GitHub Actions  
✅ **CLO5:** REPL pattern implementation  
✅ **CLO6:** Object-oriented programming principles  
✅ **CLO7:** Professional software development practices  
✅ **CLO8:** CSV file manipulation with pandas

---

## License

This project is licensed under the MIT License.

---

## Author

**Pruthul Patel**  
IS601 - Web Systems Development  
Midterm Project - Fall 2025  


---