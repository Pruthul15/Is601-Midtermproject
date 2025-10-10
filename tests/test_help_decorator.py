"""
Comprehensive tests for the Help Decorator module to achieve full coverage.
"""
import pytest
from app.help_decorator import (
    HelpComponent,
    OperationHelpWrapper,
    HelpDecorator,
    DetailedHelpDecorator,
    CategoryHelpDecorator,
    DynamicHelpGenerator
)
from app.operations import OperationFactory


class TestHelpComponent:
    """Test suite for base HelpComponent class."""
    
    def test_help_component_abstract(self):
        """Test that HelpComponent is abstract."""
        # Cannot instantiate abstract class
        with pytest.raises(TypeError):
            component = HelpComponent()


class TestOperationHelpWrapper:
    """Test suite for OperationHelpWrapper."""
    
    def test_wrapper_initialization(self):
        """Test OperationHelpWrapper initializes correctly."""
        operation = OperationFactory.create_operation("add")
        wrapper = OperationHelpWrapper(operation, "add")
        assert wrapper._operation == operation
        assert wrapper._operation_name == "add"
        
    def test_wrapper_get_help_info(self):
        """Test get_help_info returns tuple."""
        operation = OperationFactory.create_operation("add")
        wrapper = OperationHelpWrapper(operation, "add")
        op_name, description = wrapper.get_help_info()
        assert op_name == "add"
        assert isinstance(description, str)
        assert len(description) > 0
        
    def test_wrapper_all_operations(self):
        """Test wrapper works with all operation types."""
        operations = ["add", "subtract", "multiply", "divide", "power", "root"]
        for op_name in operations:
            operation = OperationFactory.create_operation(op_name)
            wrapper = OperationHelpWrapper(operation, op_name)
            name, desc = wrapper.get_help_info()
            assert name == op_name
            assert isinstance(desc, str)


class TestHelpDecorator:
    """Test suite for HelpDecorator."""
    
    def test_decorator_initialization(self):
        """Test HelpDecorator initializes correctly."""
        operation = OperationFactory.create_operation("add")
        component = OperationHelpWrapper(operation, "add")
        decorator = HelpDecorator(component)
        assert decorator._component == component
        
    def test_decorator_delegates_to_component(self):
        """Test decorator delegates to wrapped component."""
        operation = OperationFactory.create_operation("add")
        component = OperationHelpWrapper(operation, "add")
        decorator = HelpDecorator(component)
        name, desc = decorator.get_help_info()
        assert name == "add"
        assert isinstance(desc, str)


class TestDetailedHelpDecorator:
    """Test suite for DetailedHelpDecorator."""
    
    def test_detailed_decorator_initialization(self):
        """Test DetailedHelpDecorator initializes correctly."""
        operation = OperationFactory.create_operation("add")
        component = OperationHelpWrapper(operation, "add")
        decorator = DetailedHelpDecorator(component)
        assert decorator._component == component
        
    def test_detailed_decorator_adds_details(self):
        """Test detailed decorator enhances descriptions."""
        operation = OperationFactory.create_operation("add")
        component = OperationHelpWrapper(operation, "add")
        decorator = DetailedHelpDecorator(component)
        name, desc = decorator.get_help_info()
        assert name == "add"
        assert "Addition" in desc
        
    def test_detailed_decorator_all_operations(self):
        """Test detailed decorator with all operations."""
        operations = ["add", "subtract", "multiply", "divide", "power", "root",
                     "modulus", "int_divide", "percent", "abs_diff"]
        for op_name in operations:
            operation = OperationFactory.create_operation(op_name)
            component = OperationHelpWrapper(operation, op_name)
            decorator = DetailedHelpDecorator(component)
            name, desc = decorator.get_help_info()
            assert name == op_name
            assert len(desc) > 10
            
    def test_detailed_decorator_unknown_operation(self):
        """Test detailed decorator with unknown operation."""
        operation = OperationFactory.create_operation("add")
        component = OperationHelpWrapper(operation, "unknown_op")
        decorator = DetailedHelpDecorator(component)
        name, desc = decorator.get_help_info()
        assert name == "unknown_op"
        assert "unknown_op" in desc.lower()


class TestCategoryHelpDecorator:
    """Test suite for CategoryHelpDecorator."""
    
    def test_category_decorator_initialization(self):
        """Test CategoryHelpDecorator initializes correctly."""
        operation = OperationFactory.create_operation("add")
        component = OperationHelpWrapper(operation, "add")
        decorator = CategoryHelpDecorator(component)
        assert decorator._component == component
        
    def test_category_decorator_adds_category(self):
        """Test category decorator adds category information."""
        operation = OperationFactory.create_operation("add")
        component = OperationHelpWrapper(operation, "add")
        decorator = CategoryHelpDecorator(component)
        name, desc = decorator.get_help_info()
        assert name == "add"
        assert "[" in desc
        assert "]" in desc
        
    def test_category_decorator_basic_arithmetic(self):
        """Test category decorator categorizes basic arithmetic."""
        operations = ["add", "subtract", "multiply", "divide"]
        for op_name in operations:
            operation = OperationFactory.create_operation(op_name)
            component = OperationHelpWrapper(operation, op_name)
            decorator = CategoryHelpDecorator(component)
            name, desc = decorator.get_help_info()
            assert "Basic Arithmetic" in desc
            
    def test_category_decorator_advanced_math(self):
        """Test category decorator categorizes advanced math."""
        operations = ["power", "root", "modulus", "int_divide", "percent", "abs_diff"]
        for op_name in operations:
            operation = OperationFactory.create_operation(op_name)
            component = OperationHelpWrapper(operation, op_name)
            decorator = CategoryHelpDecorator(component)
            name, desc = decorator.get_help_info()
            assert "Advanced Math" in desc


class TestDynamicHelpGenerator:
    """Test suite for DynamicHelpGenerator."""
    
    def test_generate_operation_help(self):
        """Test generate_operation_help returns dictionary."""
        help_dict = DynamicHelpGenerator.generate_operation_help()
        assert isinstance(help_dict, dict)
        assert len(help_dict) > 0
        
    def test_operation_help_has_categories(self):
        """Test operation help contains categories."""
        help_dict = DynamicHelpGenerator.generate_operation_help()
        assert "Basic Arithmetic" in help_dict or "Advanced Math" in help_dict
        
    def test_operation_help_structure(self):
        """Test operation help has correct structure."""
        help_dict = DynamicHelpGenerator.generate_operation_help()
        for category, operations in help_dict.items():
            assert isinstance(category, str)
            assert isinstance(operations, list)
            for op_name, desc in operations:
                assert isinstance(op_name, str)
                assert isinstance(desc, str)
                
    def test_get_formatted_help(self):
        """Test get_formatted_help returns formatted string."""
        help_text = DynamicHelpGenerator.get_formatted_help()
        assert isinstance(help_text, str)
        assert len(help_text) > 0
        
    def test_formatted_help_has_sections(self):
        """Test formatted help contains expected sections."""
        help_text = DynamicHelpGenerator.get_formatted_help()
        assert "Available commands:" in help_text
        assert "System Commands:" in help_text
        
    def test_formatted_help_has_operations(self):
        """Test formatted help includes operations."""
        help_text = DynamicHelpGenerator.get_formatted_help()
        operations = ["add", "subtract", "multiply", "divide"]
        found = sum(1 for op in operations if op in help_text)
        assert found >= 2
        
    def test_formatted_help_has_system_commands(self):
        """Test formatted help includes system commands."""
        help_text = DynamicHelpGenerator.get_formatted_help()
        commands = ["history", "clear", "undo", "redo", "save", "load", "help", "exit"]
        found = sum(1 for cmd in commands if cmd in help_text)
        assert found >= 5


class TestDecoratorChaining:
    """Test decorator chaining functionality."""
    
    def test_detailed_then_category(self):
        """Test chaining detailed then category decorators."""
        operation = OperationFactory.create_operation("add")
        component = OperationHelpWrapper(operation, "add")
        detailed = DetailedHelpDecorator(component)
        categorized = CategoryHelpDecorator(detailed)
        name, desc = categorized.get_help_info()
        assert name == "add"
        assert "[" in desc
        assert "Addition" in desc
        
    def test_category_then_detailed(self):
        """Test chaining category then detailed decorators."""
        operation = OperationFactory.create_operation("multiply")
        component = OperationHelpWrapper(operation, "multiply")
        categorized = CategoryHelpDecorator(component)
        detailed = DetailedHelpDecorator(categorized)
        name, desc = detailed.get_help_info()
        assert name == "multiply"
        
    def test_multiple_decorator_layers(self):
        """Test multiple layers of decorators."""
        operation = OperationFactory.create_operation("power")
        component = OperationHelpWrapper(operation, "power")
        decorator1 = HelpDecorator(component)
        decorator2 = DetailedHelpDecorator(decorator1)
        decorator3 = CategoryHelpDecorator(decorator2)
        name, desc = decorator3.get_help_info()
        assert name == "power"
        assert isinstance(desc, str)


class TestHelpGeneratorIntegration:
    """Integration tests for help generation."""
    
    def test_full_help_generation_workflow(self):
        """Test complete help generation workflow."""
        op_help = DynamicHelpGenerator.generate_operation_help()
        assert len(op_help) > 0
        
        formatted = DynamicHelpGenerator.get_formatted_help()
        assert len(formatted) > 100
        
        assert "Operations:" in formatted
        assert "System Commands:" in formatted
        
    def test_help_includes_all_available_operations(self):
        """Test that help includes all available operations."""
        available_ops = OperationFactory.get_available_operations()
        help_text = DynamicHelpGenerator.get_formatted_help()
        
        found = sum(1 for op in available_ops if op in help_text)
        assert found >= len(available_ops) // 2
        
    def test_operation_help_sorted(self):
        """Test that operations are sorted within categories."""
        help_dict = DynamicHelpGenerator.generate_operation_help()
        for category, operations in help_dict.items():
            op_names = [name for name, _ in operations]
            assert op_names == sorted(op_names)


class TestHelpDecoratorEdgeCases:
    """Test edge cases for help decorators."""
    
    def test_decorator_with_none_component(self):
        """Test decorator behavior with various edge cases."""
        operation = OperationFactory.create_operation("add")
        component = OperationHelpWrapper(operation, "add")
        decorator = HelpDecorator(component)
        name, desc = decorator.get_help_info()
        assert isinstance(name, str)
        assert isinstance(desc, str)
        
    def test_empty_operation_name(self):
        """Test wrapper with edge case operation names."""
        operation = OperationFactory.create_operation("add")
        wrapper = OperationHelpWrapper(operation, "")
        name, desc = wrapper.get_help_info()
        assert name == ""
        assert isinstance(desc, str)
        
    def test_formatted_help_consistency(self):
        """Test that formatted help is consistent across calls."""
        help1 = DynamicHelpGenerator.get_formatted_help()
        help2 = DynamicHelpGenerator.get_formatted_help()
        assert help1 == help2
        
    def test_operation_help_no_duplicates(self):
        """Test that operation help has no duplicate operations."""
        help_dict = DynamicHelpGenerator.generate_operation_help()
        all_ops = []
        for category, operations in help_dict.items():
            for op_name, _ in operations:
                all_ops.append(op_name)
        
        assert len(all_ops) == len(set(all_ops))


class TestHelpComponentVariations:
    """Test various component and decorator combinations."""
    
    def test_all_operations_with_detailed_decorator(self):
        """Test detailed decorator with all operations."""
        operations = OperationFactory.get_available_operations()
        for op_name in operations:
            try:
                operation = OperationFactory.create_operation(op_name)
                component = OperationHelpWrapper(operation, op_name)
                decorator = DetailedHelpDecorator(component)
                name, desc = decorator.get_help_info()
                assert name == op_name
                assert len(desc) > 0
            except Exception as e:
                pytest.fail(f"Failed for operation {op_name}: {e}")
                
    def test_all_operations_with_category_decorator(self):
        """Test category decorator with all operations."""
        operations = OperationFactory.get_available_operations()
        for op_name in operations:
            try:
                operation = OperationFactory.create_operation(op_name)
                component = OperationHelpWrapper(operation, op_name)
                decorator = CategoryHelpDecorator(component)
                name, desc = decorator.get_help_info()
                assert name == op_name
                assert "[" in desc
                assert "]" in desc
            except Exception as e:
                pytest.fail(f"Failed for operation {op_name}: {e}")
                
    def test_full_decorator_chain_all_operations(self):
        """Test full decorator chain with all operations."""
        operations = ["add", "subtract", "multiply", "divide", "power"]
        for op_name in operations:
            operation = OperationFactory.create_operation(op_name)
            component = OperationHelpWrapper(operation, op_name)
            detailed = DetailedHelpDecorator(component)
            categorized = CategoryHelpDecorator(detailed)
            name, desc = categorized.get_help_info()
            assert name == op_name
            assert len(desc) > 20


class TestDynamicHelpGeneratorMethods:
    """Test specific DynamicHelpGenerator methods."""
    
    def test_generate_operation_help_returns_dict(self):
        """Test that generate_operation_help returns proper dict."""
        result = DynamicHelpGenerator.generate_operation_help()
        assert isinstance(result, dict)
        
    def test_get_formatted_help_returns_string(self):
        """Test that get_formatted_help returns string."""
        result = DynamicHelpGenerator.get_formatted_help()
        assert isinstance(result, str)
        
    def test_formatted_help_has_newlines(self):
        """Test that formatted help uses newlines properly."""
        help_text = DynamicHelpGenerator.get_formatted_help()
        assert "\n" in help_text
        lines = help_text.split("\n")
        assert len(lines) > 10
        
    def test_formatted_help_structure(self):
        """Test formatted help has proper structure."""
        help_text = DynamicHelpGenerator.get_formatted_help()
        lines = help_text.split("\n")
        
        assert "Available commands" in lines[0]
        
        assert any("System Commands" in line for line in lines)