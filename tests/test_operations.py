########################
# Operation Tests - Complete Coverage Including New Operations
########################

import pytest
from decimal import Decimal
from typing import Any, Dict, Type

from app.exceptions import ValidationError
from app.operations import (
    Operation,
    Addition,
    Subtraction,
    Multiplication,
    Division,
    Power,
    Root,
    Modulus,
    IntegerDivision,
    Percentage,
    AbsoluteDifference,
    OperationFactory,
)


class TestOperation:
    """Test base Operation class functionality."""

    def test_str_representation(self):
        """Test that string representation returns class name."""
        class TestOp(Operation):
            def execute(self, a: Decimal, b: Decimal) -> Decimal:
                return a

        assert str(TestOp()) == "TestOp"


class BaseOperationTest:
    """Base test class for all operations."""

    operation_class: Type[Operation]
    valid_test_cases: Dict[str, Dict[str, Any]]
    invalid_test_cases: Dict[str, Dict[str, Any]]

    def test_valid_operations(self):
        """Test operation with valid inputs."""
        operation = self.operation_class()
        for name, case in self.valid_test_cases.items():
            a = Decimal(str(case["a"]))
            b = Decimal(str(case["b"]))
            expected = Decimal(str(case["expected"]))
            result = operation.execute(a, b)
            assert result == expected, f"Failed case: {name}"

    def test_invalid_operations(self):
        """Test operation with invalid inputs raises appropriate errors."""
        operation = self.operation_class()
        for name, case in self.invalid_test_cases.items():
            a = Decimal(str(case["a"]))
            b = Decimal(str(case["b"]))
            error = case.get("error", ValidationError)
            error_message = case.get("message", "")

            with pytest.raises(error, match=error_message):
                operation.execute(a, b)


# ========================
# ORIGINAL OPERATION TESTS
# ========================

class TestAddition(BaseOperationTest):
    """Test Addition operation."""

    operation_class = Addition
    valid_test_cases = {
        "positive_numbers": {"a": "5", "b": "3", "expected": "8"},
        "negative_numbers": {"a": "-5", "b": "-3", "expected": "-8"},
        "mixed_signs": {"a": "-5", "b": "3", "expected": "-2"},
        "zero_sum": {"a": "5", "b": "-5", "expected": "0"},
        "decimals": {"a": "5.5", "b": "3.3", "expected": "8.8"},
        "large_numbers": {
            "a": "1e10",
            "b": "1e10",
            "expected": "20000000000"
        },
    }
    invalid_test_cases = {}  # Addition has no invalid cases


class TestSubtraction(BaseOperationTest):
    """Test Subtraction operation."""

    operation_class = Subtraction
    valid_test_cases = {
        "positive_numbers": {"a": "5", "b": "3", "expected": "2"},
        "negative_numbers": {"a": "-5", "b": "-3", "expected": "-2"},
        "mixed_signs": {"a": "-5", "b": "3", "expected": "-8"},
        "zero_result": {"a": "5", "b": "5", "expected": "0"},
        "decimals": {"a": "5.5", "b": "3.3", "expected": "2.2"},
        "large_numbers": {
            "a": "1e10",
            "b": "1e9",
            "expected": "9000000000"
        },
    }
    invalid_test_cases = {}  # Subtraction has no invalid cases


class TestMultiplication(BaseOperationTest):
    """Test Multiplication operation."""

    operation_class = Multiplication
    valid_test_cases = {
        "positive_numbers": {"a": "5", "b": "3", "expected": "15"},
        "negative_numbers": {"a": "-5", "b": "-3", "expected": "15"},
        "mixed_signs": {"a": "-5", "b": "3", "expected": "-15"},
        "multiply_by_zero": {"a": "5", "b": "0", "expected": "0"},
        "decimals": {"a": "5.5", "b": "3.3", "expected": "18.15"},
        "large_numbers": {
            "a": "1e5",
            "b": "1e5",
            "expected": "10000000000"
        },
    }
    invalid_test_cases = {}  # Multiplication has no invalid cases


class TestDivision(BaseOperationTest):
    """Test Division operation."""

    operation_class = Division
    valid_test_cases = {
        "positive_numbers": {"a": "6", "b": "2", "expected": "3"},
        "negative_numbers": {"a": "-6", "b": "-2", "expected": "3"},
        "mixed_signs": {"a": "-6", "b": "2", "expected": "-3"},
        "decimals": {"a": "5.5", "b": "2", "expected": "2.75"},
        "divide_zero": {"a": "0", "b": "5", "expected": "0"},
    }
    invalid_test_cases = {
        "divide_by_zero": {
            "a": "5",
            "b": "0",
            "error": ValidationError,
            "message": "Division by zero is not allowed"
        },
    }


class TestPower(BaseOperationTest):
    """Test Power operation."""

    operation_class = Power
    valid_test_cases = {
        "positive_base_and_exponent": {"a": "2", "b": "3", "expected": "8"},
        "zero_exponent": {"a": "5", "b": "0", "expected": "1"},
        "one_exponent": {"a": "5", "b": "1", "expected": "5"},
        "decimal_base": {"a": "2.5", "b": "2", "expected": "6.25"},
        "zero_base": {"a": "0", "b": "5", "expected": "0"},
    }
    invalid_test_cases = {
        "negative_exponent": {
            "a": "2",
            "b": "-3",
            "error": ValidationError,
            "message": "Negative exponents not supported"
        },
    }


class TestRoot(BaseOperationTest):
    """Test Root operation."""

    operation_class = Root
    valid_test_cases = {
        "square_root": {"a": "9", "b": "2", "expected": "3"},
        "cube_root": {"a": "27", "b": "3", "expected": "3"},
        "fourth_root": {"a": "16", "b": "4", "expected": "2"},
        "decimal_root": {"a": "2.25", "b": "2", "expected": "1.5"},
    }
    invalid_test_cases = {
        "negative_base": {
            "a": "-9",
            "b": "2",
            "error": ValidationError,
            "message": "Cannot calculate root of negative number"
        },
        "zero_root": {
            "a": "9",
            "b": "0",
            "error": ValidationError,
            "message": "Zero root is undefined"
        },
    }


# ========================
# NEW OPERATION TESTS FOR MIDTERM
# ========================

class TestModulus(BaseOperationTest):
    """Test Modulus operation - NEW FOR MIDTERM."""

    operation_class = Modulus
    valid_test_cases = {
        "positive_numbers": {"a": "10", "b": "3", "expected": "1"},
        "negative_dividend": {"a": "-10", "b": "3", "expected": "2"},
        "negative_divisor": {"a": "10", "b": "-3", "expected": "-2"},
        "zero_dividend": {"a": "0", "b": "5", "expected": "0"},
        "decimal_numbers": {"a": "10.5", "b": "3.2", "expected": "0.9"},
        "exact_division": {"a": "15", "b": "5", "expected": "0"},
    }
    invalid_test_cases = {
        "modulus_by_zero": {
            "a": "10",
            "b": "0",
            "error": ValidationError,
            "message": "Modulus by zero is not allowed"
        },
    }


class TestIntegerDivision(BaseOperationTest):
    """Test Integer Division operation - NEW FOR MIDTERM."""

    operation_class = IntegerDivision
    valid_test_cases = {
        "positive_numbers": {"a": "10", "b": "3", "expected": "3"},
        "exact_division": {"a": "15", "b": "3", "expected": "5"},
        "negative_dividend": {"a": "-10", "b": "3", "expected": "-4"},
        "negative_divisor": {"a": "10", "b": "-3", "expected": "-4"},
        "zero_dividend": {"a": "0", "b": "5", "expected": "0"},
        "decimal_truncation": {"a": "22", "b": "7", "expected": "3"},
    }
    invalid_test_cases = {
        "divide_by_zero": {
            "a": "10",
            "b": "0",
            "error": ValidationError,
            "message": "Integer division by zero is not allowed"
        },
    }


class TestPercentage(BaseOperationTest):
    """Test Percentage operation - NEW FOR MIDTERM."""

    operation_class = Percentage
    valid_test_cases = {
        "basic_percentage": {"a": "25", "b": "100", "expected": "25"},
        "greater_than_base": {"a": "150", "b": "100", "expected": "150"},
        "decimal_values": {"a": "12.5", "b": "50", "expected": "25"},
        "zero_value": {"a": "0", "b": "100", "expected": "0"},
        "negative_values": {"a": "-25", "b": "100", "expected": "-25"},
        "fractional_result": {"a": "1", "b": "3", "expected": "33.33333333333333333333333333"},
    }
    invalid_test_cases = {
        "zero_base": {
            "a": "25",
            "b": "0",
            "error": ValidationError,
            "message": "Cannot calculate percentage with zero base value"
        },
    }


class TestAbsoluteDifference(BaseOperationTest):
    """Test Absolute Difference operation - NEW FOR MIDTERM."""

    operation_class = AbsoluteDifference
    valid_test_cases = {
        "positive_difference": {"a": "10", "b": "3", "expected": "7"},
        "negative_difference": {"a": "3", "b": "10", "expected": "7"},
        "equal_numbers": {"a": "5", "b": "5", "expected": "0"},
        "negative_numbers": {"a": "-5", "b": "-8", "expected": "3"},
        "mixed_signs": {"a": "-5", "b": "3", "expected": "8"},
        "decimal_numbers": {"a": "5.7", "b": "2.3", "expected": "3.4"},
        "zero_operand": {"a": "0", "b": "5", "expected": "5"},
    }
    invalid_test_cases = {}  # Absolute difference has no invalid cases


# ========================
# OPERATION FACTORY TESTS - UPDATED FOR NEW OPERATIONS
# ========================

class TestOperationFactory:
    """Test OperationFactory functionality with all operations."""

    def test_create_all_operations(self):
        """Test creation of all valid operations including new ones."""
        operation_map = {
            'add': Addition,
            'subtract': Subtraction,
            'multiply': Multiplication,
            'divide': Division,
            'power': Power,
            'root': Root,
            'modulus': Modulus,
            'int_divide': IntegerDivision,
            'percent': Percentage,
            'abs_diff': AbsoluteDifference,
        }

        for op_name, op_class in operation_map.items():
            operation = OperationFactory.create_operation(op_name)
            assert isinstance(operation, op_class)
            # Test case-insensitive
            operation = OperationFactory.create_operation(op_name.upper())
            assert isinstance(operation, op_class)

    def test_get_available_operations_includes_new(self):
        """Test that available operations includes all new operations."""
        available = OperationFactory.get_available_operations()
        
        # Check that all operations are included
        expected_operations = [
            'add', 'subtract', 'multiply', 'divide', 'power', 'root',
            'modulus', 'int_divide', 'percent', 'abs_diff'
        ]
        
        for op in expected_operations:
            assert op in available

    def test_create_invalid_operation(self):
        """Test creation of invalid operation raises error."""
        with pytest.raises(ValueError, match="Unknown operation: invalid_op"):
            OperationFactory.create_operation("invalid_op")

    def test_register_valid_operation(self):
        """Test registering a new valid operation."""
        class NewOperation(Operation):
            def execute(self, a: Decimal, b: Decimal) -> Decimal:
                return a

        OperationFactory.register_operation("new_op", NewOperation)
        operation = OperationFactory.create_operation("new_op")
        assert isinstance(operation, NewOperation)

    def test_register_invalid_operation(self):
        """Test registering an invalid operation class raises error."""
        class InvalidOperation:
            pass

        with pytest.raises(TypeError, match="Operation class must inherit"):
            OperationFactory.register_operation("invalid", InvalidOperation)


# ========================
# INTEGRATION TESTS WITH CALCULATION MODEL
# ========================

class TestOperationIntegration:
    """Integration tests for new operations with Calculation model."""

    def test_modulus_with_calculation_model(self):
        """Test modulus operation integrates with Calculation model."""
        from app.calculation import Calculation
        
        calc = Calculation(
            operation="Modulus",
            operand1=Decimal("10"),
            operand2=Decimal("3")
        )
        assert calc.result == Decimal("1")

    def test_integer_division_with_calculation_model(self):
        """Test integer division integrates with Calculation model."""
        from app.calculation import Calculation
        
        calc = Calculation(
            operation="IntegerDivision", 
            operand1=Decimal("22"),
            operand2=Decimal("7")
        )
        assert calc.result == Decimal("3")

    def test_percentage_with_calculation_model(self):
        """Test percentage integrates with Calculation model."""
        from app.calculation import Calculation
        
        calc = Calculation(
            operation="Percentage",
            operand1=Decimal("25"),
            operand2=Decimal("100")
        )
        assert calc.result == Decimal("25")

    def test_absolute_difference_with_calculation_model(self):
        """Test absolute difference integrates with Calculation model."""
        from app.calculation import Calculation
        
        calc = Calculation(
            operation="AbsoluteDifference",
            operand1=Decimal("3"),
            operand2=Decimal("10")
        )
        assert calc.result == Decimal("7")


# ========================
# STRING REPRESENTATION TESTS FOR NEW OPERATIONS
# ========================

class TestNewOperationStringRepresentation:
    """Test string representations of new operations."""

    def test_modulus_str(self):
        """Test Modulus string representation."""
        operation = Modulus()
        assert str(operation) == "Modulus"

    def test_integer_division_str(self):
        """Test IntegerDivision string representation."""
        operation = IntegerDivision()
        assert str(operation) == "IntegerDivision"

    def test_percentage_str(self):
        """Test Percentage string representation."""
        operation = Percentage()
        assert str(operation) == "Percentage"

    def test_absolute_difference_str(self):
        """Test AbsoluteDifference string representation."""
        operation = AbsoluteDifference()
        assert str(operation) == "AbsoluteDifference"