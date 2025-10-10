"""
Comprehensive tests for the Colors module to achieve full coverage.
"""
import pytest
from unittest.mock import patch, MagicMock
from io import StringIO
import sys
from app.colors import ColorPrinter, COLORAMA_AVAILABLE


class TestColorPrinter:
    """Test suite for ColorPrinter class."""
    
    def test_colorprinter_success(self, capsys):
        """Test success method prints correct output."""
        ColorPrinter.success("Test success")
        captured = capsys.readouterr()
        assert "SUCCESS" in captured.out
        assert "Test success" in captured.out
        
    def test_colorprinter_error(self, capsys):
        """Test error method prints correct output."""
        ColorPrinter.error("Test error")
        captured = capsys.readouterr()
        assert "ERROR" in captured.out
        assert "Test error" in captured.out
        
    def test_colorprinter_warning(self, capsys):
        """Test warning method prints correct output."""
        ColorPrinter.warning("Test warning")
        captured = capsys.readouterr()
        assert "WARNING" in captured.out
        assert "Test warning" in captured.out
        
    def test_colorprinter_info(self, capsys):
        """Test info method prints correct output."""
        ColorPrinter.info("Test info")
        captured = capsys.readouterr()
        assert "INFO" in captured.out
        assert "Test info" in captured.out
        
    def test_colorprinter_operation(self, capsys):
        """Test operation method prints correct output."""
        ColorPrinter.operation("Test operation")
        captured = capsys.readouterr()
        assert "OPERATION" in captured.out
        assert "Test operation" in captured.out
        
    def test_colorprinter_result(self, capsys):
        """Test result method prints correct output."""
        ColorPrinter.result("Test result")
        captured = capsys.readouterr()
        assert "RESULT" in captured.out
        assert "Test result" in captured.out
        
    def test_colorprinter_history(self, capsys):
        """Test history method prints correct output."""
        ColorPrinter.history("Test history entry")
        captured = capsys.readouterr()
        assert "Test history entry" in captured.out
        
    def test_colorprinter_header(self, capsys):
        """Test header method prints correct output."""
        ColorPrinter.header("Test Header")
        captured = capsys.readouterr()
        assert "Test Header" in captured.out
        assert "===" in captured.out
        
    def test_colorprinter_prompt(self, capsys):
        """Test prompt method prints correct output without newline."""
        ColorPrinter.prompt("Test prompt")
        captured = capsys.readouterr()
        assert "Test prompt" in captured.out
        # Prompt includes chevron symbol
        assert "»" in captured.out


class TestColorPrinterWithoutColorama:
    """Test ColorPrinter fallback behavior when colorama not available."""
    
    @patch('app.colors.COLORAMA_AVAILABLE', False)
    def test_success_without_colorama(self, capsys):
        """Test success works without colorama."""
        ColorPrinter.success("No color success")
        captured = capsys.readouterr()
        assert "SUCCESS" in captured.out
        assert "No color success" in captured.out
        
    @patch('app.colors.COLORAMA_AVAILABLE', False)
    def test_error_without_colorama(self, capsys):
        """Test error works without colorama."""
        ColorPrinter.error("No color error")
        captured = capsys.readouterr()
        assert "ERROR" in captured.out
        assert "No color error" in captured.out
        
    @patch('app.colors.COLORAMA_AVAILABLE', False)
    def test_warning_without_colorama(self, capsys):
        """Test warning works without colorama."""
        ColorPrinter.warning("No color warning")
        captured = capsys.readouterr()
        assert "WARNING" in captured.out
        assert "No color warning" in captured.out
        
    @patch('app.colors.COLORAMA_AVAILABLE', False)
    def test_info_without_colorama(self, capsys):
        """Test info works without colorama."""
        ColorPrinter.info("No color info")
        captured = capsys.readouterr()
        assert "INFO" in captured.out
        assert "No color info" in captured.out
        
    @patch('app.colors.COLORAMA_AVAILABLE', False)
    def test_operation_without_colorama(self, capsys):
        """Test operation works without colorama."""
        ColorPrinter.operation("No color operation")
        captured = capsys.readouterr()
        assert "OPERATION" in captured.out
        assert "No color operation" in captured.out
        
    @patch('app.colors.COLORAMA_AVAILABLE', False)
    def test_result_without_colorama(self, capsys):
        """Test result works without colorama."""
        ColorPrinter.result("No color result")
        captured = capsys.readouterr()
        assert "RESULT" in captured.out
        assert "No color result" in captured.out
        
    @patch('app.colors.COLORAMA_AVAILABLE', False)
    def test_header_without_colorama(self, capsys):
        """Test header works without colorama."""
        ColorPrinter.header("No color header")
        captured = capsys.readouterr()
        assert "No color header" in captured.out
        assert "===" in captured.out
        
    @patch('app.colors.COLORAMA_AVAILABLE', False)
    def test_prompt_without_colorama(self, capsys):
        """Test prompt works without colorama."""
        ColorPrinter.prompt("No color prompt")
        captured = capsys.readouterr()
        assert "No color prompt" in captured.out


class TestColorPrinterEdgeCases:
    """Test edge cases for ColorPrinter."""
    
    def test_empty_string(self, capsys):
        """Test printing empty strings."""
        ColorPrinter.success("")
        captured = capsys.readouterr()
        assert "SUCCESS" in captured.out
        
    def test_special_characters(self, capsys):
        """Test printing special characters."""
        special = "!@#$%^&*()"
        ColorPrinter.info(special)
        captured = capsys.readouterr()
        assert special in captured.out
        
    def test_multiline_string(self, capsys):
        """Test printing multiline strings."""
        multiline = "Line 1\nLine 2\nLine 3"
        ColorPrinter.warning(multiline)
        captured = capsys.readouterr()
        assert "Line 1" in captured.out
        assert "Line 2" in captured.out
        assert "Line 3" in captured.out
        
    def test_unicode_characters(self, capsys):
        """Test printing unicode characters."""
        unicode_text = "✓ ✗ ⚠ ℹ →"
        ColorPrinter.info(unicode_text)
        captured = capsys.readouterr()
        assert "INFO" in captured.out
        
    def test_long_message(self, capsys):
        """Test printing very long messages."""
        long_msg = "A" * 1000
        ColorPrinter.success(long_msg)
        captured = capsys.readouterr()
        assert long_msg in captured.out
        
    def test_numeric_message(self, capsys):
        """Test printing numeric values."""
        ColorPrinter.result("42")
        captured = capsys.readouterr()
        assert "42" in captured.out
        assert "RESULT" in captured.out


class TestColoramaAvailability:
    """Test colorama availability flag."""
    
    def test_colorama_available_flag(self):
        """Test that COLORAMA_AVAILABLE is a boolean."""
        assert isinstance(COLORAMA_AVAILABLE, bool)
        
    def test_all_methods_callable(self):
        """Test that all ColorPrinter methods are callable."""
        assert callable(ColorPrinter.success)
        assert callable(ColorPrinter.error)
        assert callable(ColorPrinter.warning)
        assert callable(ColorPrinter.info)
        assert callable(ColorPrinter.operation)
        assert callable(ColorPrinter.result)
        assert callable(ColorPrinter.history)
        assert callable(ColorPrinter.header)
        assert callable(ColorPrinter.prompt)


class TestColorPrinterOutput:
    """Test specific output formatting."""
    
    def test_success_has_checkmark(self, capsys):
        """Test success output includes checkmark symbol."""
        ColorPrinter.success("Test")
        captured = capsys.readouterr()
        assert "✓" in captured.out
        
    def test_error_has_cross(self, capsys):
        """Test error output includes cross symbol."""
        ColorPrinter.error("Test")
        captured = capsys.readouterr()
        assert "✗" in captured.out
        
    def test_warning_has_symbol(self, capsys):
        """Test warning output includes warning symbol."""
        ColorPrinter.warning("Test")
        captured = capsys.readouterr()
        assert "⚠" in captured.out
        
    def test_info_has_symbol(self, capsys):
        """Test info output includes info symbol."""
        ColorPrinter.info("Test")
        captured = capsys.readouterr()
        assert "ℹ" in captured.out
        
    def test_operation_has_arrow(self, capsys):
        """Test operation output includes arrow symbol."""
        ColorPrinter.operation("Test")
        captured = capsys.readouterr()
        assert "→" in captured.out
        
    def test_result_has_equals(self, capsys):
        """Test result output includes equals symbol."""
        ColorPrinter.result("Test")
        captured = capsys.readouterr()
        assert "=" in captured.out
        
    def test_header_has_borders(self, capsys):
        """Test header output includes border decorations."""
        ColorPrinter.header("Test")
        captured = capsys.readouterr()
        assert "===" in captured.out
        
    def test_prompt_has_chevron(self, capsys):
        """Test prompt output includes chevron symbol."""
        ColorPrinter.prompt("Test")
        captured = capsys.readouterr()
        assert "»" in captured.out