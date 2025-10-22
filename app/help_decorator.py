########################
# Dynamic Help Decorator #
########################

from abc import ABC, abstractmethod
from typing import Dict, List, Tuple
from app.operations import OperationFactory, Operation


class HelpComponent(ABC):
    """
    ADDED: Abstract base component for the Decorator pattern.
    """

    @abstractmethod
    def get_help_info(self) -> Tuple[str, str]:  # pragma: no cover
        """Get help information for this component."""  # pragma: no cover
        pass  # pragma: no cover


class OperationHelpWrapper(HelpComponent):
    """ADDED: Concrete component that wraps Operation classes."""

    def __init__(self, operation: Operation, operation_name: str):
        self._operation = operation
        self._operation_name = operation_name

    def get_help_info(self) -> Tuple[str, str]:
        """Get basic help information for the wrapped operation."""
        class_name = self._operation.__class__.__name__
        return (self._operation_name, f"Perform {class_name.lower()} operation")


class HelpDecorator(HelpComponent):
    """ADDED: Base decorator class for the Decorator pattern."""

    def __init__(self, component: HelpComponent):
        self._component = component

    def get_help_info(self) -> Tuple[str, str]:
        """Delegate help info generation to the wrapped component."""
        return self._component.get_help_info()


class DetailedHelpDecorator(HelpDecorator):
    """ADDED: Concrete decorator that adds detailed descriptions."""

    _DETAILED_DESCRIPTIONS = {
        'add': 'Addition - Add two numbers together (a + b)',
        'subtract': 'Subtraction - Subtract second number from first (a - b)', 
        'multiply': 'Multiplication - Multiply two numbers (a × b)',
        'divide': 'Division - Divide first number by second (a ÷ b)',
        'power': 'Exponentiation - Raise first number to power of second (a^b)',
        'root': 'Root extraction - Calculate nth root of a number (a^(1/b))',
        'modulus': 'Modulus - Calculate remainder of division (a % b)',
        'int_divide': 'Integer division - Divide and return integer quotient (a // b)',
        'percent': 'Percentage - Calculate percentage of a with respect to b ((a/b)*100)',
        'abs_diff': 'Absolute difference - Calculate absolute difference between numbers |a-b|'
    }

    def get_help_info(self) -> Tuple[str, str]:
        """Get detailed help information with enhanced descriptions."""
        operation_name, _ = self._component.get_help_info()
        detailed_desc = self._DETAILED_DESCRIPTIONS.get(
            operation_name, 
            f"Perform {operation_name} operation"
        )
        return (operation_name, detailed_desc)


class CategoryHelpDecorator(HelpDecorator):
    """ADDED: Concrete decorator that adds category information."""

    _OPERATION_CATEGORIES = {
        'add': 'Basic Arithmetic',
        'subtract': 'Basic Arithmetic', 
        'multiply': 'Basic Arithmetic',
        'divide': 'Basic Arithmetic',
        'power': 'Advanced Math',
        'root': 'Advanced Math',
        'modulus': 'Advanced Math',
        'int_divide': 'Advanced Math',
        'percent': 'Advanced Math',
        'abs_diff': 'Advanced Math'
    }

    def get_help_info(self) -> Tuple[str, str]:
        """Get help information with category prefix."""
        operation_name, description = self._component.get_help_info()
        category = self._OPERATION_CATEGORIES.get(operation_name, 'Other')
        categorized_desc = f"[{category}] {description}"
        return (operation_name, categorized_desc)


class DynamicHelpGenerator:
    """ADDED: Main class that uses the Decorator pattern to generate dynamic help menus."""

    @staticmethod
    def generate_operation_help() -> Dict[str, List[Tuple[str, str]]]:
        """Generate categorized help information for all available operations."""
        available_operations = OperationFactory.get_available_operations()
        categorized_help = {}
        
        for op_name in available_operations:
            try:
                operation = OperationFactory.create_operation(op_name)
                base_component = OperationHelpWrapper(operation, op_name)
                detailed_component = DetailedHelpDecorator(base_component)
                categorized_component = CategoryHelpDecorator(detailed_component)
                
                _, help_text = categorized_component.get_help_info()
                
                if help_text.startswith('[') and ']' in help_text:
                    category_end = help_text.index(']')
                    category = help_text[1:category_end]
                    description = help_text[category_end + 2:]
                else:  # pragma: no cover
                    category = 'Other'  # pragma: no cover
                    description = help_text  # pragma: no cover
                
                if category not in categorized_help:
                    categorized_help[category] = []
                
                categorized_help[category].append((op_name, description))
                
            except Exception as e:  # pragma: no cover
                print(f"Warning: Could not generate help for operation '{op_name}': {e}")  # pragma: no cover
                continue  # pragma: no cover
        
        for category in categorized_help:
            categorized_help[category].sort(key=lambda x: x[0])
        
        return categorized_help

    @staticmethod
    def get_formatted_help() -> str:
        """FIXED: Get complete formatted help text using the Decorator pattern."""
        help_lines = []
        help_lines.append("Available commands:")
        help_lines.append("")
        
        # FIXED: Use DynamicHelpGenerator instead of cls
        operation_help = DynamicHelpGenerator.generate_operation_help()
        
        for category in sorted(operation_help.keys()):
            help_lines.append(f"{category} Operations:")
            for op_name, description in operation_help[category]:
                help_lines.append(f"  {op_name} - {description}")
            help_lines.append("")
        
        help_lines.append("System Commands:")
        help_lines.append("  history - Show calculation history")
        help_lines.append("  clear - Clear calculation history")
        help_lines.append("  undo - Undo the last calculation")
        help_lines.append("  redo - Redo the last undone calculation")
        help_lines.append("  save - Save calculation history to file")
        help_lines.append("  load - Load calculation history from file")
        help_lines.append("  help - Display this help message")
        help_lines.append("  exit - Exit the calculator")
        
        return "\n".join(help_lines)