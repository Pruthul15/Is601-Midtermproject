########################
# Command Design Pattern #
########################


from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
from decimal import Decimal

from app.calculator import Calculator
from app.operations import OperationFactory
from app.exceptions import OperationError, ValidationError
from app.colors import ColorPrinter
from app.help_decorator import DynamicHelpGenerator


class Command(ABC):
    """
    ADDED: Abstract base class for the Command pattern.
    
    The Command interface declares a method for executing a command.
    This allows us to encapsulate requests as objects, enabling parameterization
    of clients with different requests, queuing of requests, and logging operations.
    """

    @abstractmethod
    def execute(self) -> Any:
        """
        Execute the command.
        
        Returns:
            Any: Result of command execution, varies by command type
        """
        pass

    @abstractmethod
    def get_description(self) -> str:
        """
        Get a description of this command.
        
        Returns:
            str: Human-readable description of the command
        """
        pass


class CalculatorReceiver:
    """
    ADDED: Receiver class that knows how to perform calculator operations.
    
    The Receiver contains the business logic and knows how to carry out
    the operations associated with a request. In our case, this wraps
    the Calculator class and provides the actual functionality.
    """

    def __init__(self, calculator: Calculator):
        """
        Initialize receiver with calculator instance.
        
        Args:
            calculator (Calculator): The calculator instance to receive commands
        """
        self.calculator = calculator

    def perform_arithmetic(self, operation_name: str, a: str, b: str) -> str:
        """
        Perform arithmetic operation using the calculator.
        
        Args:
            operation_name (str): Name of the operation to perform
            a (str): First operand as string
            b (str): Second operand as string
            
        Returns:
            str: Formatted result of the operation
            
        Raises:
            OperationError: If operation fails
            ValidationError: If inputs are invalid
        """
        try:
            # Create and set the operation
            operation = OperationFactory.create_operation(operation_name)
            self.calculator.set_operation(operation)
            
            # Perform the calculation
            result = self.calculator.perform_operation(a, b)
            
            # Format result to avoid scientific notation
            if isinstance(result, Decimal):
                normalized = result.normalize()
                str_val = str(normalized)
                if 'E' in str_val or 'e' in str_val:
                    formatted = f"{normalized:.15f}".rstrip('0').rstrip('.')
                    if formatted == '' or formatted == '-':
                        formatted = '0'
                    return formatted
                return str_val
            return str(result)
            
        except (ValidationError, OperationError) as e:
            raise e
        except Exception as e:
            raise OperationError(f"Arithmetic operation failed: {e}")

    def show_history(self) -> List[str]:
        """Get calculator history."""
        return self.calculator.show_history()

    def clear_history(self) -> None:
        """Clear calculator history."""
        self.calculator.clear_history()

    def undo_operation(self) -> bool:
        """Undo last operation."""
        return self.calculator.undo()

    def redo_operation(self) -> bool:
        """Redo last undone operation."""
        return self.calculator.redo()

    def save_history(self) -> None:
        """Save calculator history."""
        self.calculator.save_history()

    def load_history(self) -> None:
        """Load calculator history."""
        self.calculator.load_history()


class ArithmeticCommand(Command):
    """
    ADDED: Concrete command for arithmetic operations.
    
    Encapsulates an arithmetic operation request with its parameters,
    allowing it to be passed around, queued, or logged as an object.
    """

    def __init__(self, receiver: CalculatorReceiver, operation: str, operand1: str, operand2: str):
        """
        Initialize arithmetic command.
        
        Args:
            receiver (CalculatorReceiver): The receiver that will execute the operation
            operation (str): Name of the arithmetic operation
            operand1 (str): First operand
            operand2 (str): Second operand
        """
        self.receiver = receiver
        self.operation = operation
        self.operand1 = operand1
        self.operand2 = operand2

    def execute(self) -> str:
        """
        Execute the arithmetic command.
        
        Returns:
            str: Formatted result of the arithmetic operation
        """
        result = self.receiver.perform_arithmetic(self.operation, self.operand1, self.operand2)
        
        # FIXED: Removed newlines to match test expectations
        if self.operation == 'percent':
            ColorPrinter.result(f"Result: {result}%")
        elif self.operation == 'modulus':
            ColorPrinter.result(f"Remainder: {result}")
        elif self.operation == 'int_divide':
            ColorPrinter.result(f"Integer quotient: {result}")
        elif self.operation == 'abs_diff':
            ColorPrinter.result(f"Absolute difference: {result}")
        else:
            ColorPrinter.result(f"Result: {result}")
            
        return result

    def get_description(self) -> str:
        """Get description of this arithmetic command."""
        return f"Arithmetic: {self.operation}({self.operand1}, {self.operand2})"


class SystemCommand(Command):
    """
    ADDED: Base class for system commands.
    """

    def __init__(self, receiver: CalculatorReceiver):
        """
        Initialize system command.
        
        Args:
            receiver (CalculatorReceiver): The receiver that will execute the operation
        """
        self.receiver = receiver


class HistoryCommand(SystemCommand):
    """ADDED: Concrete command for showing calculation history."""

    def execute(self) -> List[str]:
        """Execute the history command."""
        history = self.receiver.show_history()
        if not history:
            ColorPrinter.warning("No calculations in history")
        else:
            # FIXED: Removed newline to match test expectations
            ColorPrinter.header("Calculation History:")
            for i, entry in enumerate(history, 1):
                ColorPrinter.history(f"{i}. {entry}")
        return history

    def get_description(self) -> str:
        """Get description of this history command."""
        return "Display calculation history"


class ClearCommand(SystemCommand):
    """ADDED: Concrete command for clearing calculation history."""

    def execute(self) -> None:
        """Execute the clear command."""
        self.receiver.clear_history()
        ColorPrinter.success("History cleared")

    def get_description(self) -> str:
        """Get description of this clear command."""
        return "Clear calculation history"


class UndoCommand(SystemCommand):
    """ADDED: Concrete command for undoing the last operation."""

    def execute(self) -> bool:
        """Execute the undo command."""
        if self.receiver.undo_operation():
            ColorPrinter.success("Operation undone")
            return True
        else:
            ColorPrinter.warning("Nothing to undo")
            return False

    def get_description(self) -> str:
        """Get description of this undo command."""
        return "Undo the last calculation"


class RedoCommand(SystemCommand):
    """ADDED: Concrete command for redoing the last undone operation."""

    def execute(self) -> bool:
        """Execute the redo command."""
        if self.receiver.redo_operation():
            ColorPrinter.success("Operation redone")
            return True
        else:
            ColorPrinter.warning("Nothing to redo")
            return False

    def get_description(self) -> str:
        """Get description of this redo command."""
        return "Redo the last undone calculation"


class SaveCommand(SystemCommand):
    """ADDED: Concrete command for saving calculation history."""

    def execute(self) -> None:
        """Execute the save command."""
        try:
            self.receiver.save_history()
            ColorPrinter.success("History saved successfully")
        except Exception as e:
            ColorPrinter.error(f"Error saving history: {e}")

    def get_description(self) -> str:
        """Get description of this save command."""
        return "Save calculation history to file"


class LoadCommand(SystemCommand):
    """ADDED: Concrete command for loading calculation history."""

    def execute(self) -> None:
        """Execute the load command."""
        try:
            self.receiver.load_history()
            ColorPrinter.success("History loaded successfully")
        except Exception as e:
            ColorPrinter.error(f"Error loading history: {e}")

    def get_description(self) -> str:
        """Get description of this load command."""
        return "Load calculation history from file"


class HelpCommand(Command):
    """ADDED: Concrete command for displaying help using dynamic help generation."""

    def __init__(self):
        """Initialize help command."""
        pass

    def execute(self) -> str:
        """
        Execute the help command using dynamic help generation.
        
        Returns:
            str: Generated help text
        """
        # Use the DynamicHelpGenerator to create help text automatically
        help_text = DynamicHelpGenerator.get_formatted_help()
        
        # Display with colors
        for line in help_text.split('\n'):
            if line.strip() == "":
                print()
            elif 'Operations:' in line:
                ColorPrinter.header(line)
            elif line.startswith('  ') and ' - ' in line:
                # Operation or command line
                parts = line.strip().split(' - ', 1)
                if len(parts) == 2:
                    op_name, description = parts
                    if any(cmd in description.lower() for cmd in ['history', 'clear', 'undo', 'redo', 'save', 'load', 'help', 'exit']):
                        ColorPrinter.info(f"  {op_name} - {description}")
                    else:
                        ColorPrinter.operation(f"  {op_name} - {description}")
                else:
                    ColorPrinter.info(line)
            elif line.startswith('Available commands:'):
                ColorPrinter.header(line)
            elif line.startswith('System Commands:'):
                ColorPrinter.header(line)
            else:
                ColorPrinter.header(line)
        
        return help_text

    def get_description(self) -> str:
        """Get description of this help command."""
        return "Display dynamic help menu generated from available operations"


class ExitCommand(SystemCommand):
    """ADDED: Concrete command for exiting the calculator."""

    def execute(self) -> bool:
        """Execute the exit command."""
        try:
            self.receiver.save_history()
            ColorPrinter.success("History saved successfully. Goodbye!")
        except Exception as e:
            ColorPrinter.error(f"Warning: Could not save history: {e}")
            ColorPrinter.warning("Goodbye!")
        return True

    def get_description(self) -> str:
        """Get description of this exit command."""
        return "Exit the calculator application"


class CommandInvoker:
    """
    ADDED: Invoker class for the Command pattern.
    
    The Invoker knows how to execute commands but doesn't know about
    concrete command classes. It can also store commands for logging,
    queuing, or macro functionality.
    """

    def __init__(self):
        """Initialize command invoker with empty command history."""
        self.command_history: List[Command] = []

    def execute_command(self, command: Command) -> Any:
        """
        Execute a command and store it in history.
        
        Args:
            command (Command): The command to execute
            
        Returns:
            Any: Result of command execution
        """
        # Store command in history for potential macro/replay functionality
        self.command_history.append(command)
        
        # Execute the command
        return command.execute()

    def get_command_history(self) -> List[str]:
        """
        Get descriptions of all executed commands.
        
        Returns:
            List[str]: List of command descriptions
        """
        return [cmd.get_description() for cmd in self.command_history]


class CommandFactory:
    """
    ADDED: Factory for creating command objects.
    
    Simplifies command creation and provides a centralized location
    for command instantiation logic.
    """

    @staticmethod
    def create_arithmetic_command(receiver: CalculatorReceiver, operation: str, operand1: str, operand2: str) -> ArithmeticCommand:
        """Create an arithmetic command."""
        return ArithmeticCommand(receiver, operation, operand1, operand2)

    @staticmethod
    def create_system_command(command_type: str, receiver: CalculatorReceiver) -> Command:
        """
        Create a system command based on type.
        
        Args:
            command_type (str): Type of system command
            receiver (CalculatorReceiver): The receiver for the command
            
        Returns:
            Command: Appropriate command instance
            
        Raises:
            ValueError: If command type is unknown
        """
        command_map = {
            'history': HistoryCommand,
            'clear': ClearCommand,
            'undo': UndoCommand,
            'redo': RedoCommand,
            'save': SaveCommand,
            'load': LoadCommand,
            'exit': ExitCommand
        }
        
        if command_type == 'help':
            return HelpCommand()
        
        command_class = command_map.get(command_type)
        if not command_class:
            raise ValueError(f"Unknown command type: {command_type}")
            
        return command_class(receiver)