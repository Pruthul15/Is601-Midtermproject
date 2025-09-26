########################
# Input Validation     #
########################

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Any
from app.calculator_config import CalculatorConfig
from app.exceptions import ValidationError


@dataclass
class InputValidator:
    """
    Validates and sanitizes calculator inputs.
    
    This class provides static methods for validating user inputs to ensure
    they meet the required criteria before processing.
    """
    
    @staticmethod
    def validate_number(value: Any, config: CalculatorConfig) -> Decimal:
        """
        Validate and convert input to Decimal.
        
        This method takes user input in various formats and converts it to a 
        validated Decimal number suitable for mathematical operations.
        
        Args:
            value: Input value to validate - can be string, int, float, or Decimal
            config: Calculator configuration with validation parameters
            
        Returns:
            Decimal: Validated and converted number, normalized for display
            
        Raises:
            ValidationError: If input is invalid, non-numeric, or exceeds limits
        """
        try:
            # Handle string inputs by stripping whitespace
            if isinstance(value, str):
                value = value.strip()
                
            # Convert to Decimal for precise arithmetic
            number = Decimal(str(value))
            
            # Check if the number exceeds the maximum allowed value
            if abs(number) > config.max_input_value:
                raise ValidationError(f"Value exceeds maximum allowed: {config.max_input_value}")
                
            # Return normalized decimal (removes trailing zeros)
            return number.normalize()
            
        except InvalidOperation as e:
            # Handle cases where conversion to Decimal fails
            raise ValidationError(f"Invalid number format: {value}") from e