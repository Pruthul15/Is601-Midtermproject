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


def calculator_repl():
    """
    Command-line interface for the calculator with colorama support.

    Implements a Read-Eval-Print Loop (REPL) that continuously prompts the user
    for commands, processes arithmetic operations, and manages calculation history.
    UPDATED: Enhanced with new operations for midterm requirements and color-coded outputs.
    """
    try:
        # Initialize the Calculator instance
        calc = Calculator()

        # Register observers for logging and auto-saving history
        calc.add_observer(LoggingObserver())
        calc.add_observer(AutoSaveObserver(calc))

        ColorPrinter.header("Calculator started. Type 'help' for commands.")

        while True:
            try:
                # Prompt the user for a command
                ColorPrinter.prompt("\nEnter command: ")
                command = input().lower().strip()

                if command == 'help':
                    # Display available commands - UPDATED with new operations and colors
                    ColorPrinter.header("\nAvailable commands:")
                    ColorPrinter.operation("  add, subtract, multiply, divide, power, root - Perform calculations")
                    ColorPrinter.operation("  modulus - Remainder of division (a % b)")
                    ColorPrinter.operation("  int_divide - Integer division (a // b)")
                    ColorPrinter.operation("  percent - Percentage calculation ((a / b) * 100)")
                    ColorPrinter.operation("  abs_diff - Absolute difference |a - b|")
                    ColorPrinter.info("  history - Show calculation history")
                    ColorPrinter.info("  clear - Clear calculation history")
                    ColorPrinter.info("  undo - Undo the last calculation")
                    ColorPrinter.info("  redo - Redo the last undone calculation")
                    ColorPrinter.warning("  save - Save calculation history to file")
                    ColorPrinter.warning("  load - Load calculation history from file")
                    ColorPrinter.header("  help - Display this help message")
                    ColorPrinter.header("  exit - Exit the calculator")
                    continue

                if command == 'exit':
                    # Attempt to save history before exiting
                    try:
                        calc.save_history()
                        ColorPrinter.success("History saved successfully. Goodbye!")
                    except Exception as e:
                        ColorPrinter.error(f"Warning: Could not save history: {e}")
                        ColorPrinter.warning("Goodbye!")
                    break

                if command == 'history':
                    # Display calculation history
                    history = calc.show_history()
                    if not history:
                        ColorPrinter.warning("No calculations in history")
                    else:
                        ColorPrinter.header("\nCalculation History:")
                        for i, entry in enumerate(history, 1):
                            ColorPrinter.history(f"{i}. {entry}")
                    continue

                if command == 'clear':
                    # Clear calculation history
                    calc.clear_history()
                    ColorPrinter.success("History cleared")
                    continue

                if command == 'undo':
                    # Undo the last calculation
                    if calc.undo():
                        ColorPrinter.success("Operation undone")
                    else:
                        ColorPrinter.warning("Nothing to undo")
                    continue

                if command == 'redo':
                    # Redo the last undone calculation
                    if calc.redo():
                        ColorPrinter.success("Operation redone")
                    else:
                        ColorPrinter.warning("Nothing to redo")
                    continue

                if command == 'save':
                    # Save calculation history to file
                    try:
                        calc.save_history()
                        ColorPrinter.success("History saved successfully")
                    except Exception as e:
                        ColorPrinter.error(f"Error saving history: {e}")
                    continue

                if command == 'load':
                    # Load calculation history from file
                    try:
                        calc.load_history()
                        ColorPrinter.success("History loaded successfully")
                    except Exception as e:
                        ColorPrinter.error(f"Error loading history: {e}")
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

                        # Create the appropriate operation instance using the Factory pattern
                        operation = OperationFactory.create_operation(command)
                        calc.set_operation(operation)

                        # Perform the calculation
                        result = calc.perform_operation(a, b)

                        # FIXED: Format result to avoid scientific notation and normalize decimals
                        def format_for_display(value):
                            """
                            FIXED: Format numbers without scientific notation and normalize decimals.
                            
                            This function handles two main issues:
                            1. Prevents scientific notation display (1E+1 becomes 10)
                            2. Normalizes decimals to remove trailing zeros (5.000 becomes 5)
                            
                            Args:
                                value: The number to format (usually Decimal)
                                
                            Returns:
                                str: Clean formatted number string
                            """
                            if isinstance(value, Decimal):
                                # FIXED: First normalize the decimal to remove trailing zeros (5.000 -> 5)
                                normalized = value.normalize()
                                str_val = str(normalized)
                                # FIXED: If contains scientific notation, format differently to show normal numbers
                                if 'E' in str_val or 'e' in str_val:
                                    # Convert scientific notation to normal decimal notation
                                    formatted = f"{normalized:.15f}".rstrip('0').rstrip('.')
                                    # Handle edge case where all zeros are stripped
                                    if formatted == '' or formatted == '-':
                                        formatted = '0'
                                    return formatted
                                else:
                                    # Return normal string representation
                                    return str_val
                            return str(value)

                        formatted_result = format_for_display(result)

                        # Display operation-specific result messages - UPDATED for new operations with colors
                        if command == 'percent':
                            # FIXED: Limit percentage precision for readability
                            try:
                                # Round to 2 decimal places for percentages to avoid excessive precision
                                if isinstance(result, Decimal):
                                    rounded_result = round(float(result), 2)
                                    ColorPrinter.result(f"\nResult: {rounded_result}%")
                                else:
                                    ColorPrinter.result(f"\nResult: {formatted_result}%")
                            except:
                                # Fallback if rounding fails
                                ColorPrinter.result(f"\nResult: {formatted_result}%")
                        elif command == 'modulus':
                            ColorPrinter.result(f"\nRemainder: {formatted_result}")
                        elif command == 'int_divide':
                            ColorPrinter.result(f"\nInteger quotient: {formatted_result}")
                        elif command == 'abs_diff':
                            ColorPrinter.result(f"\nAbsolute difference: {formatted_result}")
                        else:
                            ColorPrinter.result(f"\nResult: {formatted_result}")
                            
                    except (ValidationError, OperationError) as e:
                        # Handle known exceptions related to validation or operation errors
                        ColorPrinter.error(f"Error: {e}")
                    except Exception as e:
                        # Handle any unexpected exceptions
                        ColorPrinter.error(f"Unexpected error: {e}")
                    continue

                # Handle unknown commands
                ColorPrinter.error(f"Unknown command: '{command}'. Type 'help' for available commands.")

            except KeyboardInterrupt:
                # Handle Ctrl+C interruption gracefully
                ColorPrinter.warning("\nOperation cancelled")
                continue
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