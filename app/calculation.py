########################
# Calculation Model    #
########################

from dataclasses import dataclass, field
import datetime
from decimal import Decimal, InvalidOperation
import logging
from typing import Any, Dict

from app.exceptions import OperationError


@dataclass
class Calculation:
    """
    Value Object representing a single calculation.

    This class encapsulates the details of a mathematical calculation, including the
    operation performed, operands involved, the result, and the timestamp of the
    calculation. It provides methods for performing the calculation, serializing
    the data for storage, and deserializing data to recreate a Calculation instance.
    """

    # Required fields
    operation: str          # The name of the operation (e.g., "Addition")
    operand1: Decimal       # The first operand in the calculation
    operand2: Decimal       # The second operand in the calculation

    # Fields with default values
    result: Decimal = field(init=False)  # The result of the calculation, computed post-initialization
    timestamp: datetime.datetime = field(default_factory=datetime.datetime.now)  # Time when the calculation was performed

    def __post_init__(self):
        """
        Post-initialization processing.

        Automatically calculates the result of the operation after the Calculation
        instance is created.
        """
        self.result = self.calculate()

    def _calculate_modulus(self, x: Decimal, y: Decimal) -> Decimal:
        """
        Calculate modulus using precision-preserving Decimal arithmetic.
        
        This method matches the logic from operations.py to ensure consistency
        between live calculations and stored history.
        
        Args:
            x (Decimal): Dividend
            y (Decimal): Divisor
            
        Returns:
            Decimal: Remainder with correct Python behavior and preserved precision
        """
        # Calculate using Decimal arithmetic to preserve precision
        quotient = x / y
        
        # Get integer part of quotient (floor for negative numbers to match Python behavior)
        if quotient < 0:
            # For negative quotient, use floor behavior like Python's //
            integer_part = int(quotient) - 1 if quotient != int(quotient) else int(quotient)
        else:
            # For positive quotient, normal truncation
            integer_part = int(quotient)
        
        # Calculate remainder: x - (y * integer_part)
        remainder = x - (y * Decimal(integer_part))
        
        return remainder

    def calculate(self) -> Decimal:
        """
        Execute calculation using the specified operation.

        Utilizes a dictionary to map operation names to their corresponding
        lambda functions, enabling dynamic execution of operations based on
        the operation name.

        Returns:
            Decimal: The result of the calculation.

        Raises:
            OperationError: If the operation is unknown or the calculation fails.
        """
        # Mapping of operation names to their corresponding functions
        # UPDATED: Added new operations for midterm requirements with precision-preserving modulus
        operations = {
            # Basic operations
            "Addition": lambda x, y: x + y,
            "Subtraction": lambda x, y: x - y,
            "Multiplication": lambda x, y: x * y,
            "Division": lambda x, y: x / y if y != 0 else self._raise_div_zero(),
            "Power": lambda x, y: Decimal(pow(float(x), float(y))) if y >= 0 else self._raise_neg_power(),
            "Root": lambda x, y: (
                Decimal(pow(float(x), 1 / float(y))) 
                if x >= 0 and y != 0 
                else self._raise_invalid_root(x, y)
            ),
            # New operations for midterm - FIXED MODULUS TO PRESERVE PRECISION
            "Modulus": lambda x, y: (
                self._calculate_modulus(x, y) if y != 0 else self._raise_mod_zero()
            ),
            "IntegerDivision": lambda x, y: (
                Decimal(str(int(float(x) // float(y)))) if y != 0 else self._raise_int_div_zero()
            ),
            "Percentage": lambda x, y: (x / y) * Decimal('100') if y != 0 else self._raise_percent_zero(),
            "AbsoluteDifference": lambda x, y: abs(x - y)
        }

        # Retrieve the operation function based on the operation name
        op = operations.get(self.operation)
        if not op:
            raise OperationError(f"Unknown operation: {self.operation}")

        try:
            # Execute the operation with the provided operands
            return op(self.operand1, self.operand2)
        except (InvalidOperation, ValueError, ArithmeticError) as e:
            # Handle any errors that occur during calculation
            raise OperationError(f"Calculation failed: {str(e)}")

    @staticmethod
    def _raise_div_zero():  # pragma: no cover
        """
        Helper method to raise division by zero error.

        This method is called when a division by zero is attempted.
        """
        raise OperationError("Division by zero is not allowed")

    @staticmethod
    def _raise_neg_power():  # pragma: no cover
        """
        Helper method to raise negative power error.

        This method is called when a negative exponent is used in a power operation.
        """
        raise OperationError("Negative exponents are not supported")

    @staticmethod
    def _raise_invalid_root(x: Decimal, y: Decimal):  # pragma: no cover
        """
        Helper method to raise invalid root error.

        This method is called when an invalid root operation is attempted, such as
        taking the root of a negative number or using zero as the root degree.

        Args:
            x (Decimal): The number from which the root is taken.
            y (Decimal): The degree of the root.
        """
        if y == 0:
            raise OperationError("Zero root is undefined")
        if x < 0:
            raise OperationError("Cannot calculate root of negative number")
        raise OperationError("Invalid root operation")

    # NEW HELPER METHODS FOR MIDTERM OPERATIONS
    @staticmethod
    def _raise_mod_zero():  # pragma: no cover
        """
        Helper method to raise modulus by zero error.

        This method is called when a modulus by zero is attempted.
        """
        raise OperationError("Modulus by zero is not allowed")

    @staticmethod
    def _raise_int_div_zero():  # pragma: no cover
        """
        Helper method to raise integer division by zero error.

        This method is called when an integer division by zero is attempted.
        """
        raise OperationError("Integer division by zero is not allowed")

    @staticmethod
    def _raise_percent_zero():  # pragma: no cover
        """
        Helper method to raise percentage calculation with zero base error.

        This method is called when percentage calculation has zero as base value.
        """
        raise OperationError("Cannot calculate percentage with zero base value")

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert calculation to dictionary for serialization.

        This method transforms the Calculation instance into a dictionary format,
        facilitating easy storage and retrieval (e.g., saving to a file).

        Returns:
            Dict[str, Any]: A dictionary containing the calculation data in a serializable format.
        """
        return {
            'operation': self.operation,
            'operand1': str(self.operand1),
            'operand2': str(self.operand2),
            'result': str(self.result),
            'timestamp': self.timestamp.isoformat()
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Calculation':
        """
        Create calculation from dictionary.

        This method reconstructs a Calculation instance from a dictionary, ensuring
        that all required fields are present and correctly formatted.

        Args:
            data (Dict[str, Any]): Dictionary containing calculation data.

        Returns:
            Calculation: A new instance of Calculation with data populated from the dictionary.

        Raises:
            OperationError: If data is invalid or missing required fields.
        """
        try:
            # Create the calculation object with the original operands
            calc = Calculation(
                operation=data['operation'],
                operand1=Decimal(data['operand1']),
                operand2=Decimal(data['operand2'])
            )

            # Set the timestamp from the saved data
            calc.timestamp = datetime.datetime.fromisoformat(data['timestamp'])

            # Verify the result matches (helps catch data corruption)
            saved_result = Decimal(data['result'])
            if calc.result != saved_result:
                logging.warning(
                    f"Loaded calculation result {saved_result} "
                    f"differs from computed result {calc.result}"
                )  # pragma: no cover

            return calc

        except (KeyError, InvalidOperation, ValueError) as e:
            raise OperationError(f"Invalid calculation data: {str(e)}")

    def __str__(self) -> str:
        """
        Return string representation of calculation.

        Provides a human-readable representation of the calculation, showing the
        operation performed and its result.

        Returns:
            str: Formatted string showing the calculation and result.
        """
        return f"{self.operation}({self.operand1}, {self.operand2}) = {self.result}"

    def __repr__(self) -> str:
        """
        Return detailed string representation of calculation.

        Provides a detailed and unambiguous string representation of the Calculation
        instance, useful for debugging.

        Returns:
            str: Detailed string showing all calculation attributes.
        """
        return (
            f"Calculation(operation='{self.operation}', "
            f"operand1={self.operand1}, "
            f"operand2={self.operand2}, "
            f"result={self.result}, "
            f"timestamp='{self.timestamp.isoformat()}')"
        )

    def __eq__(self, other: object) -> bool:
        """
        Check if two calculations are equal.

        Compares two Calculation instances to determine if they represent the same
        operation with identical operands and results.

        Args:
            other (object): Another calculation to compare with.

        Returns:
            bool: True if calculations are equal, False otherwise.
        """
        if not isinstance(other, Calculation):
            return NotImplemented
        return (
            self.operation == other.operation and
            self.operand1 == other.operand1 and
            self.operand2 == other.operand2 and
            self.result == other.result
        )

    def format_result(self, precision: int = 10) -> str:
        """
        Format the calculation result with specified precision.

        This method formats the result to a fixed number of decimal places,
        removing any trailing zeros for a cleaner presentation.

        Args:
            precision (int, optional): Number of decimal places to show. Defaults to 10.

        Returns:
            str: Formatted string representation of the result.
        """
        try:
            # Remove trailing zeros and format to specified precision
            return str(self.result.normalize().quantize(
                Decimal('0.' + '0' * precision)
            ).normalize())
        except InvalidOperation:  # pragma: no cover
            return str(self.result)