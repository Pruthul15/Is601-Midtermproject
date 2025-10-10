"""
Comprehensive tests for the Command Pattern module to achieve full coverage.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from app.command_pattern import (
    Command,
    CalculatorReceiver,
    ArithmeticCommand,
    SystemCommand,
    HistoryCommand,
    ClearCommand,
    UndoCommand,
    RedoCommand,
    SaveCommand,
    LoadCommand,
    HelpCommand,
    ExitCommand,
    CommandInvoker,
    CommandFactory
)
from app.calculator import Calculator
from app.exceptions import ValidationError, OperationError


class TestCommand:
    """Test suite for base Command class."""
    
    def test_command_is_abstract(self):
        """Test that Command is an abstract base class."""
        # Cannot instantiate abstract class
        with pytest.raises(TypeError):
            command = Command()


class TestCalculatorReceiver:
    """Test suite for CalculatorReceiver."""
    
    def test_receiver_initialization(self):
        """Test CalculatorReceiver initializes correctly."""
        calculator = Calculator()
        receiver = CalculatorReceiver(calculator)
        assert receiver.calculator == calculator
        
    def test_receiver_perform_arithmetic_add(self):
        """Test arithmetic operation through receiver."""
        calculator = Calculator()
        receiver = CalculatorReceiver(calculator)
        result = receiver.perform_arithmetic("add", "5", "3")
        assert result == "8"
        
    def test_receiver_perform_arithmetic_all_operations(self):
        """Test all arithmetic operations through receiver."""
        calculator = Calculator()
        receiver = CalculatorReceiver(calculator)
        
        operations = [
            ("add", "10", "5", "15"),
            ("subtract", "10", "5", "5"),
            ("multiply", "10", "5", "50"),
            ("divide", "10", "5", "2"),
            ("power", "2", "3", "8"),
            ("root", "27", "3", "3"),
            ("modulus", "10", "3", "1"),
            ("int_divide", "10", "3", "3"),
            ("percent", "50", "200", "25"),
            ("abs_diff", "10", "15", "5"),
        ]
        
        for op_name, a, b, expected in operations:
            result = receiver.perform_arithmetic(op_name, a, b)
            assert result == expected
            
    def test_receiver_show_history(self):
        """Test show_history method."""
        calculator = Calculator()
        receiver = CalculatorReceiver(calculator)
        receiver.perform_arithmetic("add", "5", "3")
        history = receiver.show_history()
        assert len(history) > 0
        
    def test_receiver_clear_history(self):
        """Test clear_history method."""
        calculator = Calculator()
        receiver = CalculatorReceiver(calculator)
        receiver.perform_arithmetic("add", "5", "3")
        receiver.clear_history()
        assert len(receiver.show_history()) == 0
        
    def test_receiver_undo_operation(self):
        """Test undo operation."""
        calculator = Calculator()
        receiver = CalculatorReceiver(calculator)
        receiver.perform_arithmetic("add", "5", "3")
        result = receiver.undo_operation()
        assert result is True
        
    def test_receiver_redo_operation(self):
        """Test redo operation."""
        calculator = Calculator()
        receiver = CalculatorReceiver(calculator)
        receiver.perform_arithmetic("add", "5", "3")
        calculator.undo()
        result = receiver.redo_operation()
        assert result is True
        
    def test_receiver_save_history(self):
        """Test save_history method."""
        calculator = Calculator()
        receiver = CalculatorReceiver(calculator)
        receiver.perform_arithmetic("add", "5", "3")
        receiver.save_history()
        
    def test_receiver_load_history(self):
        """Test load_history method."""
        calculator = Calculator()
        receiver = CalculatorReceiver(calculator)
        receiver.load_history()


class TestArithmeticCommand:
    """Test suite for ArithmeticCommand."""
    
    def test_arithmetic_command_initialization(self):
        """Test ArithmeticCommand initializes correctly."""
        calculator = Calculator()
        receiver = CalculatorReceiver(calculator)
        command = ArithmeticCommand(receiver, "add", "5", "3")
        assert command.receiver == receiver
        assert command.operation == "add"
        assert command.operand1 == "5"
        assert command.operand2 == "3"
        
    def test_arithmetic_command_execute(self, capsys):
        """Test execute method of ArithmeticCommand."""
        calculator = Calculator()
        receiver = CalculatorReceiver(calculator)
        command = ArithmeticCommand(receiver, "add", "5", "3")
        result = command.execute()
        assert result == "8"
        
    def test_arithmetic_command_execute_all_operations(self):
        """Test all operation types."""
        calculator = Calculator()
        receiver = CalculatorReceiver(calculator)
        
        operations = [
            ("add", "10", "5", "15"),
            ("subtract", "10", "5", "5"),
            ("multiply", "10", "5", "50"),
            ("divide", "10", "5", "2"),
            ("power", "2", "3", "8"),
            ("root", "27", "3", "3"),
            ("modulus", "10", "3", "1"),
            ("int_divide", "10", "3", "3"),
            ("percent", "50", "200", "25"),
            ("abs_diff", "10", "15", "5"),
        ]
        
        for op_name, a, b, expected in operations:
            command = ArithmeticCommand(receiver, op_name, a, b)
            result = command.execute()
            assert result == expected
        
    def test_arithmetic_command_get_description(self):
        """Test get_description method."""
        calculator = Calculator()
        receiver = CalculatorReceiver(calculator)
        command = ArithmeticCommand(receiver, "multiply", "4", "7")
        description = command.get_description()
        assert "Arithmetic" in description
        assert "multiply" in description


class TestSystemCommand:
    """Test suite for SystemCommand."""
    
    def test_system_command_initialization(self):
        """Test SystemCommand initializes correctly."""
        calculator = Calculator()
        receiver = CalculatorReceiver(calculator)
        command = HistoryCommand(receiver)
        assert command.receiver == receiver


class TestHistoryCommand:
    """Test suite for HistoryCommand."""
    
    def test_history_command_empty(self, capsys):
        """Test history command with empty history."""
        calculator = Calculator()
        receiver = CalculatorReceiver(calculator)
        command = HistoryCommand(receiver)
        result = command.execute()
        assert isinstance(result, list)
        
    def test_history_command_with_data(self, capsys):
        """Test history command with calculations."""
        calculator = Calculator()
        receiver = CalculatorReceiver(calculator)
        receiver.perform_arithmetic("add", "5", "3")
        receiver.perform_arithmetic("multiply", "4", "2")
        command = HistoryCommand(receiver)
        result = command.execute()
        assert len(result) >= 2
        
    def test_history_command_get_description(self):
        """Test get_description method."""
        calculator = Calculator()
        receiver = CalculatorReceiver(calculator)
        command = HistoryCommand(receiver)
        description = command.get_description()
        assert "history" in description.lower()


class TestClearCommand:
    """Test suite for ClearCommand."""
    
    def test_clear_command_execute(self, capsys):
        """Test clear command execution."""
        calculator = Calculator()
        receiver = CalculatorReceiver(calculator)
        receiver.perform_arithmetic("add", "5", "3")
        command = ClearCommand(receiver)
        command.execute()
        assert len(calculator.history) == 0
        
    def test_clear_command_get_description(self):
        """Test get_description method."""
        calculator = Calculator()
        receiver = CalculatorReceiver(calculator)
        command = ClearCommand(receiver)
        description = command.get_description()
        assert "clear" in description.lower()


class TestUndoCommand:
    """Test suite for UndoCommand."""
    
    def test_undo_command_success(self, capsys):
        """Test successful undo."""
        calculator = Calculator()
        receiver = CalculatorReceiver(calculator)
        receiver.perform_arithmetic("add", "5", "3")
        command = UndoCommand(receiver)
        result = command.execute()
        assert result is True
        
    def test_undo_command_nothing_to_undo(self, capsys):
        """Test undo with empty history."""
        calculator = Calculator()
        receiver = CalculatorReceiver(calculator)
        command = UndoCommand(receiver)
        result = command.execute()
        assert result is False
        
    def test_undo_command_multiple_times(self):
        """Test multiple undo operations."""
        calculator = Calculator()
        receiver = CalculatorReceiver(calculator)
        receiver.perform_arithmetic("add", "5", "3")
        receiver.perform_arithmetic("add", "10", "20")
        receiver.perform_arithmetic("add", "1", "1")
        
        command = UndoCommand(receiver)
        command.execute()
        command.execute()
        
        assert len(calculator.history) >= 1
        
    def test_undo_command_get_description(self):
        """Test get_description method."""
        calculator = Calculator()
        receiver = CalculatorReceiver(calculator)
        command = UndoCommand(receiver)
        description = command.get_description()
        assert "undo" in description.lower()


class TestRedoCommand:
    """Test suite for RedoCommand."""
    
    def test_redo_command_success(self, capsys):
        """Test successful redo."""
        calculator = Calculator()
        receiver = CalculatorReceiver(calculator)
        receiver.perform_arithmetic("add", "5", "3")
        calculator.undo()
        command = RedoCommand(receiver)
        result = command.execute()
        assert result is True
        
    def test_redo_command_nothing_to_redo(self, capsys):
        """Test redo with nothing to redo."""
        calculator = Calculator()
        receiver = CalculatorReceiver(calculator)
        command = RedoCommand(receiver)
        result = command.execute()
        assert result is False
        
    def test_redo_command_after_multiple_undo(self):
        """Test redo after multiple undo operations."""
        calculator = Calculator()
        receiver = CalculatorReceiver(calculator)
        receiver.perform_arithmetic("add", "5", "3")
        receiver.perform_arithmetic("add", "10", "20")
        calculator.undo()
        calculator.undo()
        
        command = RedoCommand(receiver)
        command.execute()
        
        assert len(calculator.history) >= 1
        
    def test_redo_command_get_description(self):
        """Test get_description method."""
        calculator = Calculator()
        receiver = CalculatorReceiver(calculator)
        command = RedoCommand(receiver)
        description = command.get_description()
        assert "redo" in description.lower()


class TestSaveCommand:
    """Test suite for SaveCommand."""
    
    def test_save_command_execute(self, capsys):
        """Test save command execution."""
        calculator = Calculator()
        receiver = CalculatorReceiver(calculator)
        receiver.perform_arithmetic("add", "5", "3")
        command = SaveCommand(receiver)
        command.execute()
        
    def test_save_command_get_description(self):
        """Test get_description method."""
        calculator = Calculator()
        receiver = CalculatorReceiver(calculator)
        command = SaveCommand(receiver)
        description = command.get_description()
        assert "save" in description.lower()


class TestLoadCommand:
    """Test suite for LoadCommand."""
    
    def test_load_command_execute(self, capsys):
        """Test load command execution."""
        calculator = Calculator()
        receiver = CalculatorReceiver(calculator)
        command = LoadCommand(receiver)
        command.execute()
        
    def test_load_command_get_description(self):
        """Test get_description method."""
        calculator = Calculator()
        receiver = CalculatorReceiver(calculator)
        command = LoadCommand(receiver)
        description = command.get_description()
        assert "load" in description.lower()


class TestHelpCommand:
    """Test suite for HelpCommand."""
    
    def test_help_command_execute(self, capsys):
        """Test help command execution."""
        command = HelpCommand()
        result = command.execute()
        assert isinstance(result, str)
        assert len(result) > 0
        
    def test_help_command_get_description(self):
        """Test get_description method."""
        command = HelpCommand()
        description = command.get_description()
        assert "help" in description.lower()


class TestExitCommand:
    """Test suite for ExitCommand."""
    
    def test_exit_command_execute(self, capsys):
        """Test exit command execution."""
        calculator = Calculator()
        receiver = CalculatorReceiver(calculator)
        command = ExitCommand(receiver)
        result = command.execute()
        assert result is True
        
    def test_exit_command_get_description(self):
        """Test get_description method."""
        calculator = Calculator()
        receiver = CalculatorReceiver(calculator)
        command = ExitCommand(receiver)
        description = command.get_description()
        assert "exit" in description.lower()


class TestCommandInvoker:
    """Test suite for CommandInvoker."""
    
    def test_invoker_initialization(self):
        """Test CommandInvoker initializes correctly."""
        invoker = CommandInvoker()
        assert invoker.command_history == []
        
    def test_invoker_execute_command(self):
        """Test execute_command method."""
        calculator = Calculator()
        receiver = CalculatorReceiver(calculator)
        invoker = CommandInvoker()
        command = ArithmeticCommand(receiver, "add", "5", "3")
        result = invoker.execute_command(command)
        assert result == "8"
        assert len(invoker.command_history) == 1
        
    def test_invoker_get_command_history(self):
        """Test get_command_history method."""
        calculator = Calculator()
        receiver = CalculatorReceiver(calculator)
        invoker = CommandInvoker()
        command1 = ArithmeticCommand(receiver, "add", "5", "3")
        command2 = ArithmeticCommand(receiver, "multiply", "4", "2")
        invoker.execute_command(command1)
        invoker.execute_command(command2)
        history = invoker.get_command_history()
        assert len(history) == 2


class TestCommandFactory:
    """Test suite for CommandFactory."""
    
    def test_factory_create_arithmetic_command(self):
        """Test create_arithmetic_command method."""
        calculator = Calculator()
        receiver = CalculatorReceiver(calculator)
        command = CommandFactory.create_arithmetic_command(receiver, "add", "5", "3")
        assert isinstance(command, ArithmeticCommand)
        
    def test_factory_create_system_commands(self):
        """Test create_system_command for all system command types."""
        calculator = Calculator()
        receiver = CalculatorReceiver(calculator)
        
        command_types = ['history', 'clear', 'undo', 'redo', 'save', 'load', 'exit']
        for cmd_type in command_types:
            command = CommandFactory.create_system_command(cmd_type, receiver)
            assert isinstance(command, Command)
            
    def test_factory_create_help_command(self):
        """Test create_system_command for help."""
        calculator = Calculator()
        receiver = CalculatorReceiver(calculator)
        command = CommandFactory.create_system_command('help', receiver)
        assert isinstance(command, HelpCommand)
        
    def test_factory_invalid_command_type(self):
        """Test create_system_command with invalid type."""
        calculator = Calculator()
        receiver = CalculatorReceiver(calculator)
        with pytest.raises(ValueError):
            CommandFactory.create_system_command('invalid', receiver)


class TestCommandPatternIntegration:
    """Integration tests for command pattern."""
    
    def test_full_command_workflow(self):
        """Test complete command pattern workflow."""
        calculator = Calculator()
        receiver = CalculatorReceiver(calculator)
        invoker = CommandInvoker()
        
        # Perform operations
        add_cmd = ArithmeticCommand(receiver, "add", "10", "5")
        add_result = invoker.execute_command(add_cmd)
        assert add_result == "15"
        
        mult_cmd = ArithmeticCommand(receiver, "multiply", "3", "4")
        mult_result = invoker.execute_command(mult_cmd)
        assert mult_result == "12"
        
        # Check history
        hist_cmd = HistoryCommand(receiver)
        history = invoker.execute_command(hist_cmd)
        assert len(history) >= 2