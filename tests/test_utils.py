"""Tests for utility functions."""

import pytest
from quantum_password_analyzer.utils import (
    ensure_dir,
    factor_str,
    seconds_to_text,
    text_to_seconds,
)


class TestTimeConversion:
    """Test time conversion functions."""

    def test_text_to_seconds(self):
        """Test converting text durations to seconds."""
        test_cases = [
            ("Instantly", 0.0),
            ("instantly", 0.0),
            ("1 second", 1.0),
            ("2 seconds", 2.0),
            ("1 minute", 60.0),
            ("2.5 minutes", 150.0),
            ("1 hour", 3600.0),
            ("1 day", 86400.0),
            ("1 week", 604800.0),
            ("1 month", 2592000.0),
            ("1 year", 31557600.0),
            ("10k seconds", 10000.0),
            ("5m years", 5000000 * 31557600.0),
        ]

        for input_text, expected_seconds in test_cases:
            assert text_to_seconds(input_text) == expected_seconds

    def test_invalid_text_to_seconds(self):
        """Test handling of invalid text durations."""
        with pytest.raises(ValueError):
            text_to_seconds("invalid")

        with pytest.raises(ValueError):
            text_to_seconds("10 lightyears")

    def test_seconds_to_text(self):
        """Test converting seconds to text durations."""
        test_cases = [
            (0.0, "Instantly"),
            (0.2, "Instantly"),
            (1.0, "1 second"),
            (2.0, "2 seconds"),
            (60.0, "1 minute"),
            (150.0, "2.5 minutes"),
            (3600.0, "1 hour"),
            (86400.0, "1 day"),
            (604800.0, "1 week"),
            (2592000.0, "1 month"),
            (31557600.0, "1 year"),
            (10000.0, "2.8 hours"),
            (5000000 * 31557600.0, "5m years"),
        ]

        for input_seconds, expected_text in test_cases:
            assert seconds_to_text(input_seconds) == expected_text


def test_factor_str():
    """Test conversion of factors to filename-friendly strings."""
    assert factor_str(100) == "100"
    assert factor_str(100.0) == "100"
    assert factor_str(100.5) == "100_5"
    assert factor_str(0.25) == "0_25"


def test_ensure_dir(tmp_path):
    """Test directory creation and validation."""
    # Test with existing directory
    result = ensure_dir(tmp_path)
    assert result == tmp_path
    assert result.exists()

    # Test with non-existing directory
    new_dir = tmp_path / "new_dir"
    result = ensure_dir(new_dir)
    assert result == new_dir
    assert result.exists()

    # Test with nested directory
    nested_dir = tmp_path / "parent" / "child" / "grandchild"
    result = ensure_dir(nested_dir)
    assert result == nested_dir
    assert result.exists()
