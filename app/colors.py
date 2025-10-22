# Filename: app/colors.py

"""
Color-coded terminal output using colorama library.

This module provides colored text output for enhanced user experience.
Implements one of the optional advanced features for the midterm project.
Falls back to plain text if colorama is not installed.

References:
- https://www.geeksforgeeks.org/python/introduction-to-python-colorama/
- Colorama documentation: https://pypi.org/project/colorama/
"""

try:
    from colorama import Fore, Back, Style, init
    # Initialize colorama with autoreset=True so colors automatically reset after each print
    # This prevents color bleeding into subsequent prints
    init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:  # pragma: no cover
    # If colorama is not installed, fall back to plain text output
    # This only runs if colorama dependency is missing in the environment
    COLORAMA_AVAILABLE = False  # pragma: no cover


class ColorPrinter:
    """
    Enhanced printer class with colorama support for colored terminal output.
    
    Provides methods for different message types with appropriate colors:
    - Success messages: Green
    - Error messages: Red
    - Warning messages: Yellow
    - Info messages: Cyan
    - Operation messages: Magenta
    - Result messages: Bright Green
    - History entries: White
    - Headers: Bright Blue with bold style
    - Prompts: Blue
    
    If colorama is not available, falls back to plain text with Unicode symbols.
    """
    
    @staticmethod
    def success(message):
        """
        Print success message in green color.
        
        Args:
            message (str): The success message to display
        """
        if COLORAMA_AVAILABLE:
            print(f"{Fore.GREEN}✓ SUCCESS: {message}{Style.RESET_ALL}")
        else:  # pragma: no cover
            print(f"✓ SUCCESS: {message}")  # pragma: no cover
    
    @staticmethod
    def error(message):
        """
        Print error message in red color.
        
        Args:
            message (str): The error message to display
        """
        if COLORAMA_AVAILABLE:
            print(f"{Fore.RED}✗ ERROR: {message}{Style.RESET_ALL}")
        else:  # pragma: no cover
            print(f"✗ ERROR: {message}")  # pragma: no cover
    
    @staticmethod
    def warning(message):
        """
        Print warning message in yellow color.
        
        Args:
            message (str): The warning message to display
        """
        if COLORAMA_AVAILABLE:
            print(f"{Fore.YELLOW}⚠ WARNING: {message}{Style.RESET_ALL}")
        else:  # pragma: no cover
            print(f"⚠ WARNING: {message}")  # pragma: no cover
    
    @staticmethod
    def info(message):
        """
        Print informational message in cyan color.
        
        Args:
            message (str): The info message to display
        """
        if COLORAMA_AVAILABLE:
            print(f"{Fore.CYAN}ℹ INFO: {message}{Style.RESET_ALL}")
        else:  # pragma: no cover
            print(f"ℹ INFO: {message}")  # pragma: no cover
    
    @staticmethod
    def operation(message):
        """
        Print operation message in magenta color.
        
        Args:
            message (str): The operation message to display
        """
        if COLORAMA_AVAILABLE:
            print(f"{Fore.MAGENTA}→ OPERATION: {message}{Style.RESET_ALL}")
        else:  # pragma: no cover
            print(f"→ OPERATION: {message}")  # pragma: no cover
    
    @staticmethod
    def result(message):
        """
        Print calculation result in bright green color.
        
        Args:
            message (str): The result message to display
        """
        if COLORAMA_AVAILABLE:
            print(f"{Fore.LIGHTGREEN_EX}= RESULT: {message}{Style.RESET_ALL}")
        else:  # pragma: no cover
            print(f"= RESULT: {message}")  # pragma: no cover
    
    @staticmethod
    def history(message):
        """
        Print history entry in white color.
        
        Args:
            message (str): The history entry to display
        """
        if COLORAMA_AVAILABLE:
            print(f"{Fore.WHITE}  {message}{Style.RESET_ALL}")
        else:  # pragma: no cover
            print(f"  {message}")  # pragma: no cover
    
    @staticmethod
    def header(message):
        """
        Print section header in bright blue with bold style.
        
        Args:
            message (str): The header text to display
        """
        if COLORAMA_AVAILABLE:
            print(f"{Fore.LIGHTBLUE_EX}{Style.BRIGHT}=== {message} ==={Style.RESET_ALL}")
        else:  # pragma: no cover
            print(f"=== {message} ===")  # pragma: no cover
    
    @staticmethod
    def prompt(message):
        """
        Print user input prompt in blue color without newline.
        
        Args:
            message (str): The prompt text to display
        """
        if COLORAMA_AVAILABLE:
            print(f"{Fore.BLUE}» {message}{Style.RESET_ALL}", end="")
        else:  # pragma: no cover
            print(f"» {message}", end="")  # pragma: no cover


# Example usage (for testing purposes)
if __name__ == "__main__":  # pragma: no cover
    """Demonstrate all color output types."""
    printer = ColorPrinter()  # pragma: no cover
    
    print("\nColorama Color Test:\n")  # pragma: no cover
    printer.header("Calculator Color Demo")  # pragma: no cover
    printer.success("Operation completed successfully")  # pragma: no cover
    printer.error("Division by zero detected")  # pragma: no cover
    printer.warning("Input value approaching maximum limit")  # pragma: no cover
    printer.info("Loading calculation history...")  # pragma: no cover
    printer.operation("add")  # pragma: no cover
    printer.result("Result: 42")  # pragma: no cover
    printer.history("1. Addition(5, 3) = 8")  # pragma: no cover
    printer.prompt("Enter command: ")  # pragma: no cover
    print("\n")  # pragma: no cover