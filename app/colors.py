# app/colors.py - Simple version without colorama dependency
"""Simple color printer without external dependencies."""

class ColorPrinter:
    """Simple printer that works without colorama dependency."""
    
    @staticmethod
    def success(message):
        print(f"✓ SUCCESS: {message}")
    
    @staticmethod
    def error(message):
        print(f"✗ ERROR: {message}")
    
    @staticmethod
    def warning(message):
        print(f"⚠ WARNING: {message}")
    
    @staticmethod
    def info(message):
        print(f"ℹ INFO: {message}")
    
    @staticmethod
    def operation(message):
        print(f"→ OPERATION: {message}")
    
    @staticmethod
    def result(message):
        print(f"= RESULT: {message}")
    
    @staticmethod
    def history(message):
        print(f"  {message}")
    
    @staticmethod
    def header(message):
        print(f"=== {message} ===")
    
    @staticmethod
    def prompt(message):
        print(f"» {message}", end="")