########################
# Calculator REPL       #
########################

from decimal import Decimal
import logging

from app.calculator import Calculator
from app.exceptions import OperationError, ValidationError
from app.history import AutoSaveObserver, LoggingObserver
from app.operations import OperationFactory
from app.colors import ColorPrinter  # NEW IMPORT

# ADDED: Import optional design patterns for midterm A grade requirements
from app.help_decorator import DynamicHelpGenerator
from app.command_pattern import (
    CommandInvoker, CommandFactory, CalculatorReceiver, HelpCommand
)


def calculator_repl():
    """
    Command-line interface for the calculator with colorama support.

    Implements a Read-Eval-Print Loop (REPL) that continuously prompts the user
    for commands, processes arithmetic operations, and manages calculation history.
    UPDATED: Enhanced with new operations for midterm requirements and color-coded outputs.
    
    ADDED: Now includes TWO optional design patterns for A grade:
    1. DECORATOR PATTERN: Dynamic help menu that auto-updates when operations are added
    2. COMMAND PATTERN: Encapsulates requests as objects for better flexibility
    """
    try:
        # Initialize the Calculator instance
        calc = Calculator()

        # Register observers for logging and auto-saving history
        calc.add_observer(LoggingObserver())
        calc.add_observer(AutoSaveObserver(calc))

        # ADDED: Command pattern setup for midterm optional feature
        receiver = CalculatorReceiver(calc)
        invoker = CommandInvoker()

        ColorPrinter.header("Calculator started. Type 'help' for commands.")
        # ADDED: Indicate enhanced features are available
        ColorPrinter.info("Enhanced with Dynamic Help (Decorator Pattern) and Command Pattern!")

        while True:
            try:
                # Prompt the user for a command
                ColorPrinter.prompt("\nEnter command: ")
                command = input().lower().strip()

                if command == 'help':
                    # ADDED: Use dynamic help generation with Decorator pattern instead of manual help
                    # This automatically generates help from available operations!
                    help_command = HelpCommand()
                    invoker.execute_command(help_command)
                    continue

                if command == 'exit':
                    # ADDED: Use Command pattern for exit instead of direct calculator calls
                    exit_command = CommandFactory.create_system_command('exit', receiver)
                    invoker.execute_command(exit_command)
                    break

                if command == 'history':
                    # ADDED: Use Command pattern for history instead of direct calculator calls
                    history_command = CommandFactory.create_system_command('history', receiver)
                    invoker.execute_command(history_command)
                    continue

                if command == 'clear':
                    # ADDED: Use Command pattern for clear instead of direct calculator calls
                    clear_command = CommandFactory.create_system_command('clear', receiver)
                    invoker.execute_command(clear_command)
                    continue

                if command == 'undo':
                    # ADDED: Use Command pattern for undo instead of direct calculator calls
                    undo_command = CommandFactory.create_system_command('undo', receiver)
                    invoker.execute_command(undo_command)
                    continue

                if command == 'redo':
                    # ADDED: Use Command pattern for redo instead of direct calculator calls
                    redo_command = CommandFactory.create_system_command('redo', receiver)
                    invoker.execute_command(redo_command)
                    continue

                if command == 'save':
                    # ADDED: Use Command pattern for save instead of direct calculator calls
                    save_command = CommandFactory.create_system_command('save', receiver)
                    invoker.execute_command(save_command)
                    continue

                if command == 'load':
                    # ADDED: Use Command pattern for load instead of direct calculator calls
                    load_command = CommandFactory.create_system_command('load', receiver)
                    invoker.execute_command(load_command)
                    continue

                # Check if command is a valid operation - UPDATED to use dynamic operation list
                available_operations = OperationFactory.get_available_operations()
                if command in available_operations:
                    # Perform the specified arithmetic operation
                    try:
                        ColorPrinter.operation(f"\nPerforming {command} operation:")
                        ColorPrinter.info("Enter numbers (or 'cancel' to abort):")
                        
                        # Get first operand
                        ColorPrinter.prompt("First number: ")
                        a = input()
                        if a.lower() == 'cancel':
                            ColorPrinter.warning("Operation cancelled")
                            continue
                            
                        # Get second operand
                        ColorPrinter.prompt("Second number: ")
                        b = input()
                        if b.lower() == 'cancel':
                            ColorPrinter.warning("Operation cancelled")
                            continue

                        # ADDED: Use Command pattern for arithmetic operations instead of direct calculator calls
                        arithmetic_command = CommandFactory.create_arithmetic_command(
                            receiver, command, a, b
                        )
                        result = invoker.execute_command(arithmetic_command)
                            
                    except (ValidationError, OperationError) as e:
                        # Handle known exceptions related to validation or operation errors
                        ColorPrinter.error(f"Error: {e}")
                    except Exception as e:
                        # Handle any unexpected exceptions
                        ColorPrinter.error(f"Unexpected error: {e}")
                    continue

                # Handle unknown commands
                ColorPrinter.error(f"Unknown command: '{command}'. Type 'help' for available commands.")

            except KeyboardInterrupt:  # pragma: no cover
                # Handle Ctrl+C interruption gracefully - hard to test in automated tests
                ColorPrinter.warning("\nOperation cancelled")  # pragma: no cover
                continue  # pragma: no cover
            except EOFError:
                # Handle end-of-file (e.g., Ctrl+D) gracefully
                ColorPrinter.warning("\nInput terminated. Exiting...")
                break
            except Exception as e:
                # Handle any other unexpected exceptions
                ColorPrinter.error(f"Error: {e}")
                continue

    except Exception as e:
        # Handle fatal errors during initialization
        ColorPrinter.error(f"Fatal error: {e}")
        logging.error(f"Fatal error in calculator REPL: {e}")
        raise