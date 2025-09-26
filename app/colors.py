# app/colors.py
"""
Color utility module for the calculator application.
Provides colored output functionality using colorama.
Based on: https://www.geeksforgeeks.org/python/introduction-to-python-colorama/
"""

from colorama import Fore, Back, Style, init

# Initialize colorama for cross-platform support
init(autoreset=True)

class Colors:
    """Color utility class for consistent colored output."""
    
    # Text colors
    SUCCESS = Fore.GREEN
    ERROR = Fore.RED
    WARNING = Fore.YELLOW
    INFO = Fore.CYAN
    OPERATION = Fore.BLUE
    RESULT = Fore.MAGENTA
    HISTORY = Fore.WHITE
    PROMPT = Fore.LIGHTWHITE_EX
    
    # Background colors (optional)
    ERROR_BG = Back.RED
    SUCCESS_BG = Back.GREEN
    
    # Styles
    BOLD = Style.BRIGHT
    DIM = Style.DIM
    RESET = Style.RESET_ALL

class ColorPrinter:
    """Utility class for printing colored messages."""
    
    @staticmethod
    def success(message):
        """Print a success message in green."""
        print(f"{Colors.SUCCESS}{message}{Colors.RESET}")
    
    @staticmethod
    def error(message):
        """Print an error message in red."""
        print(f"{Colors.ERROR}{message}{Colors.RESET}")
    
    @staticmethod
    def warning(message):
        """Print a warning message in yellow."""
        print(f"{Colors.WARNING}{message}{Colors.RESET}")
    
    @staticmethod
    def info(message):
        """Print an info message in cyan."""
        print(f"{Colors.INFO}{message}{Colors.RESET}")
    
    @staticmethod
    def operation(message):
        """Print an operation message in blue."""
        print(f"{Colors.OPERATION}{message}{Colors.RESET}")
    
    @staticmethod
    def result(message):
        """Print a result message in magenta and bold."""
        print(f"{Colors.RESULT}{Colors.BOLD}{message}{Colors.RESET}")
    
    @staticmethod
    def history(message):
        """Print a history message in white."""
        print(f"{Colors.HISTORY}{message}{Colors.RESET}")
    
    @staticmethod
    def header(message):
        """Print a header message with bold cyan."""
        print(f"{Colors.INFO}{Colors.BOLD}{message}{Colors.RESET}")
    
    @staticmethod
    def prompt(message):
        """Print a prompt message in bright white without newline."""
        print(f"{Colors.PROMPT}{Colors.BOLD}{message}{Colors.RESET}", end="")