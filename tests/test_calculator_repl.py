########################
# REPL Tests - Comprehensive Coverage with Colorama Support
########################

import pytest
from unittest.mock import Mock, patch, MagicMock
from io import StringIO
import sys

from app.calculator_repl import calculator_repl
from app.exceptions import OperationError, ValidationError


class TestCalculatorREPL:
    """Test suite for calculator REPL functionality with colorama support."""

    def test_help_command(self):
        """Test help command displays all available commands."""
        with patch('builtins.input', side_effect=['help', 'exit']):
            with patch('app.calculator_repl.ColorPrinter.header') as mock_header:
                with patch('app.calculator_repl.ColorPrinter.operation') as mock_operation:
                    with patch('app.calculator_repl.ColorPrinter.info') as mock_info:
                        with patch('app.calculator_repl.ColorPrinter.warning') as mock_warning:
                            with patch('app.calculator_repl.ColorPrinter.success'):
                                with patch('app.calculator.Calculator.save_history'):
                                    calculator_repl()
                    
                                    # Verify help text is displayed
                                    mock_header.assert_any_call("\nAvailable commands:")
                                    mock_operation.assert_any_call("  add, subtract, multiply, divide, power, root - Perform calculations")
                                    mock_info.assert_any_call("  history - Show calculation history")

    def test_exit_with_save_success(self):
        """Test normal exit with successful history save."""
        with patch('builtins.input', side_effect=['exit']):
            with patch('app.calculator_repl.ColorPrinter.success') as mock_success:
                with patch('app.calculator.Calculator.save_history') as mock_save:
                    calculator_repl()
                    
                    mock_save.assert_called_once()
                    mock_success.assert_any_call("History saved successfully. Goodbye!")

    def test_exit_with_save_error(self):
        """Test exit when save_history raises an exception."""
        with patch('builtins.input', side_effect=['exit']):
            with patch('app.calculator_repl.ColorPrinter.error') as mock_error:
                with patch('app.calculator_repl.ColorPrinter.warning') as mock_warning:
                    with patch('app.calculator.Calculator.save_history', side_effect=Exception("Save error")):
                        calculator_repl()
                        
                        mock_error.assert_any_call("Warning: Could not save history: Save error")
                        mock_warning.assert_any_call("Goodbye!")

    def test_history_empty(self):
        """Test history command when no calculations exist."""
        with patch('builtins.input', side_effect=['history', 'exit']):
            with patch('app.calculator_repl.ColorPrinter.warning') as mock_warning:
                with patch('app.calculator_repl.ColorPrinter.success'):
                    with patch('app.calculator.Calculator.show_history', return_value=[]):
                        calculator_repl()
                        
                        mock_warning.assert_any_call("No calculations in history")

    def test_history_with_calculations(self):
        """Test history command when calculations exist."""
        mock_history = ["Addition(2, 3) = 5", "Subtraction(10, 4) = 6"]
        
        with patch('builtins.input', side_effect=['history', 'exit']):
            with patch('app.calculator_repl.ColorPrinter.header') as mock_header:
                with patch('app.calculator_repl.ColorPrinter.history') as mock_history_print:
                    with patch('app.calculator_repl.ColorPrinter.success'):
                        with patch('app.calculator.Calculator.show_history', return_value=mock_history):
                            calculator_repl()
                            
                            mock_header.assert_any_call("\nCalculation History:")
                            mock_history_print.assert_any_call("1. Addition(2, 3) = 5")
                            mock_history_print.assert_any_call("2. Subtraction(10, 4) = 6")

    def test_clear_history(self):
        """Test clear history command."""
        with patch('builtins.input', side_effect=['clear', 'exit']):
            with patch('app.calculator_repl.ColorPrinter.success') as mock_success:
                with patch('app.calculator.Calculator.clear_history') as mock_clear:
                    calculator_repl()
                    
                    mock_clear.assert_called_once()
                    mock_success.assert_any_call("History cleared")

    def test_undo_success(self):
        """Test successful undo operation."""
        with patch('builtins.input', side_effect=['undo', 'exit']):
            with patch('app.calculator_repl.ColorPrinter.success') as mock_success:
                with patch('app.calculator.Calculator.undo', return_value=True):
                    calculator_repl()
                    
                    mock_success.assert_any_call("Operation undone")

    def test_undo_nothing_to_undo(self):
        """Test undo when nothing to undo."""
        with patch('builtins.input', side_effect=['undo', 'exit']):
            with patch('app.calculator_repl.ColorPrinter.warning') as mock_warning:
                with patch('app.calculator_repl.ColorPrinter.success'):
                    with patch('app.calculator.Calculator.undo', return_value=False):
                        calculator_repl()
                        
                        mock_warning.assert_any_call("Nothing to undo")

    def test_redo_success(self):
        """Test successful redo operation."""
        with patch('builtins.input', side_effect=['redo', 'exit']):
            with patch('app.calculator_repl.ColorPrinter.success') as mock_success:
                with patch('app.calculator.Calculator.redo', return_value=True):
                    calculator_repl()
                    
                    mock_success.assert_any_call("Operation redone")

    def test_redo_nothing_to_redo(self):
        """Test redo when nothing to redo."""
        with patch('builtins.input', side_effect=['redo', 'exit']):
            with patch('app.calculator_repl.ColorPrinter.warning') as mock_warning:
                with patch('app.calculator_repl.ColorPrinter.success'):
                    with patch('app.calculator.Calculator.redo', return_value=False):
                        calculator_repl()
                        
                        mock_warning.assert_any_call("Nothing to redo")

    def test_save_command_success(self):
        """Test save command successful execution."""
        with patch('builtins.input', side_effect=['save', 'exit']):
            with patch('app.calculator_repl.ColorPrinter.success') as mock_success:
                with patch('app.calculator.Calculator.save_history') as mock_save:
                    calculator_repl()
                    
                    # save_history called twice: once for save command, once for exit
                    assert mock_save.call_count == 2
                    mock_success.assert_any_call("History saved successfully")

    def test_save_command_error(self):
        """Test save command when exception occurs."""
        with patch('builtins.input', side_effect=['save', 'exit']):
            with patch('app.calculator_repl.ColorPrinter.error') as mock_error:
                with patch('app.calculator_repl.ColorPrinter.success'):
                    with patch('app.calculator.Calculator.save_history', side_effect=Exception("Save failed")):
                        calculator_repl()
                        
                        mock_error.assert_any_call("Error saving history: Save failed")

    def test_load_command_success(self):
        """Test load command successful execution."""
        with patch('builtins.input', side_effect=['load', 'exit']):
            with patch('app.calculator_repl.ColorPrinter.success') as mock_success:
                with patch('app.calculator.Calculator.load_history') as mock_load:
                    calculator_repl()
                    
                    # load_history called twice: once during init, once for load command
                    assert mock_load.call_count == 2
                    mock_success.assert_any_call("History loaded successfully")

    def test_load_command_error(self):
        """Test load command when exception occurs."""
        with patch('builtins.input', side_effect=['load', 'exit']):
            with patch('app.calculator_repl.ColorPrinter.error') as mock_error:
                with patch('app.calculator_repl.ColorPrinter.success'):
                    with patch('app.calculator.Calculator.load_history', side_effect=Exception("Load failed")):
                        calculator_repl()
                        
                        mock_error.assert_any_call("Error loading history: Load failed")

    def test_arithmetic_operation_success(self):
        """Test successful arithmetic operation."""
        from decimal import Decimal
        
        with patch('builtins.input', side_effect=['add', '2', '3', 'exit']):
            with patch('app.calculator_repl.ColorPrinter.result') as mock_result:
                with patch('app.calculator_repl.ColorPrinter.success'):
                    with patch('app.calculator.Calculator.perform_operation', return_value=Decimal('5')):
                        calculator_repl()
                        
                        mock_result.assert_any_call("\nResult: 5")

    def test_operation_cancel_first_number(self):
        """Test canceling operation at first number."""
        with patch('builtins.input', side_effect=['add', 'cancel', 'exit']):
            with patch('app.calculator_repl.ColorPrinter.warning') as mock_warning:
                with patch('app.calculator_repl.ColorPrinter.success'):
                    calculator_repl()
                    
                    mock_warning.assert_any_call("Operation cancelled")

    def test_operation_cancel_second_number(self):
        """Test canceling operation at second number."""
        with patch('builtins.input', side_effect=['add', '2', 'cancel', 'exit']):
            with patch('app.calculator_repl.ColorPrinter.warning') as mock_warning:
                with patch('app.calculator_repl.ColorPrinter.success'):
                    calculator_repl()
                    
                    mock_warning.assert_any_call("Operation cancelled")

    def test_operation_validation_error(self):
        """Test operation with validation error."""
        with patch('builtins.input', side_effect=['add', '2', '3', 'exit']):
            with patch('app.calculator_repl.ColorPrinter.error') as mock_error:
                with patch('app.calculator_repl.ColorPrinter.success'):
                    with patch('app.calculator.Calculator.perform_operation', side_effect=ValidationError("Invalid input")):
                        calculator_repl()
                        
                        mock_error.assert_any_call("Error: Invalid input")

    def test_operation_operation_error(self):
        """Test operation with operation error."""
        with patch('builtins.input', side_effect=['add', '2', '3', 'exit']):
            with patch('app.calculator_repl.ColorPrinter.error') as mock_error:
                with patch('app.calculator_repl.ColorPrinter.success'):
                    with patch('app.calculator.Calculator.perform_operation', side_effect=OperationError("Operation failed")):
                        calculator_repl()
                        
                        mock_error.assert_any_call("Error: Operation failed")

    def test_operation_unexpected_error(self):
        """Test operation with unexpected error."""
        with patch('builtins.input', side_effect=['add', '2', '3', 'exit']):
            with patch('app.calculator_repl.ColorPrinter.error') as mock_error:
                with patch('app.calculator_repl.ColorPrinter.success'):
                    with patch('app.calculator.Calculator.perform_operation', side_effect=RuntimeError("Unexpected error")):
                        calculator_repl()
                        
                        mock_error.assert_any_call("Unexpected error: Unexpected error")

    def test_unknown_command(self):
        """Test unknown command handling."""
        with patch('builtins.input', side_effect=['invalid_command', 'exit']):
            with patch('app.calculator_repl.ColorPrinter.error') as mock_error:
                with patch('app.calculator_repl.ColorPrinter.success'):
                    calculator_repl()
                    
                    mock_error.assert_any_call("Unknown command: 'invalid_command'. Type 'help' for available commands.")

    def test_keyboard_interrupt(self):
        """Test KeyboardInterrupt (Ctrl+C) handling."""
        with patch('builtins.input', side_effect=[KeyboardInterrupt(), 'exit']):
            with patch('app.calculator_repl.ColorPrinter.warning') as mock_warning:
                with patch('app.calculator_repl.ColorPrinter.success'):
                    calculator_repl()
                    
                    mock_warning.assert_any_call("\nOperation cancelled")

    def test_eof_error(self):
        """Test EOFError (Ctrl+D) handling."""
        with patch('builtins.input', side_effect=[EOFError()]):
            with patch('app.calculator_repl.ColorPrinter.warning') as mock_warning:
                calculator_repl()
                
                mock_warning.assert_any_call("\nInput terminated. Exiting...")

    def test_unexpected_error_in_loop(self):
        """Test unexpected error in main loop."""
        with patch('builtins.input', side_effect=[RuntimeError("Unexpected"), 'exit']):
            with patch('app.calculator_repl.ColorPrinter.error') as mock_error:
                with patch('app.calculator_repl.ColorPrinter.success'):
                    calculator_repl()
                    
                    mock_error.assert_any_call("Error: Unexpected")

    @patch('app.calculator_repl.logging.error')
    def test_fatal_initialization_error(self, mock_logging_error):
        """Test fatal error during initialization."""
        with patch('app.calculator_repl.Calculator', side_effect=Exception("Fatal init error")):
            with patch('app.calculator_repl.ColorPrinter.error') as mock_error:
                with pytest.raises(Exception, match="Fatal init error"):
                    calculator_repl()
                    
                mock_error.assert_any_call("Fatal error: Fatal init error")
                mock_logging_error.assert_called_once()

    def test_all_arithmetic_operations(self):
        """Test all arithmetic operations for complete coverage."""
        operations = ['add', 'subtract', 'multiply', 'divide', 'power', 'root']
        
        for op in operations:
            with patch('builtins.input', side_effect=[op, '2', '3', 'exit']):
                with patch('app.calculator_repl.ColorPrinter.result'):
                    with patch('app.calculator_repl.ColorPrinter.success'):
                        with patch('app.calculator.Calculator.perform_operation', return_value=1):
                            calculator_repl()

    def test_decimal_result_normalization(self):
        """Test Decimal result normalization."""
        from decimal import Decimal
        
        with patch('builtins.input', side_effect=['add', '2', '3', 'exit']):
            with patch('app.calculator_repl.ColorPrinter.result') as mock_result:
                with patch('app.calculator_repl.ColorPrinter.success'):
                    # Return a Decimal that needs normalization
                    mock_result_value = Decimal('5.000')
                    with patch('app.calculator.Calculator.perform_operation', return_value=mock_result_value):
                        calculator_repl()
                        
                        # Should normalize 5.000 to 5
                        mock_result.assert_any_call("\nResult: 5")

    def test_modulus_operation_display(self):
        """Test modulus operation result display."""
        from decimal import Decimal
        
        with patch('builtins.input', side_effect=['modulus', '10', '3', 'exit']):
            with patch('app.calculator_repl.ColorPrinter.result') as mock_result:
                with patch('app.calculator_repl.ColorPrinter.success'):
                    with patch('app.calculator.Calculator.perform_operation', return_value=Decimal('1')):
                        calculator_repl()
                        
                        mock_result.assert_any_call("\nRemainder: 1")

    def test_int_divide_operation_display(self):
        """Test integer division operation result display."""
        from decimal import Decimal
        
        with patch('builtins.input', side_effect=['int_divide', '10', '3', 'exit']):
            with patch('app.calculator_repl.ColorPrinter.result') as mock_result:
                with patch('app.calculator_repl.ColorPrinter.success'):
                    with patch('app.calculator.Calculator.perform_operation', return_value=Decimal('3')):
                        calculator_repl()
                        
                        mock_result.assert_any_call("\nInteger quotient: 3")

    def test_percent_operation_display(self):
        """Test percentage operation result display."""
        from decimal import Decimal
        
        with patch('builtins.input', side_effect=['percent', '25', '100', 'exit']):
            with patch('app.calculator_repl.ColorPrinter.result') as mock_result:
                with patch('app.calculator_repl.ColorPrinter.success'):
                    with patch('app.calculator.Calculator.perform_operation', return_value=Decimal('25')):
                        calculator_repl()
                        
                        mock_result.assert_any_call("\nResult: 25.0%")

    def test_abs_diff_operation_display(self):
        """Test absolute difference operation result display."""
        from decimal import Decimal
        
        with patch('builtins.input', side_effect=['abs_diff', '5', '3', 'exit']):
            with patch('app.calculator_repl.ColorPrinter.result') as mock_result:
                with patch('app.calculator_repl.ColorPrinter.success'):
                    with patch('app.calculator.Calculator.perform_operation', return_value=Decimal('2')):
                        calculator_repl()
                        
                        mock_result.assert_any_call("\nAbsolute difference: 2")