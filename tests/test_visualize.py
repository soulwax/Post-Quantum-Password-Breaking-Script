"""Tests for visualization functions."""

import os
from pathlib import Path

import matplotlib
import pandas as pd
import pytest

# Use non-interactive backend for testing
matplotlib.use("Agg")

from quantum_password_analyzer.visualize import create_infographic


@pytest.fixture
def sample_csv_file(tmp_path):
    """Create a sample CSV file for testing."""
    csv_path = tmp_path / "100_output.csv"
    sample_data = """Number of Characters,Numbers Only,Lowercase Letters,Upper and Lowercase Letters
4,Instantly,1 second,5 seconds
6,1 second,1 minute,1 hour
8,2 minutes,1 day,1 year
"""
    csv_path.write_text(sample_data)
    return csv_path


def test_create_infographic(sample_csv_file, tmp_path):
    """Test infographic creation."""
    output_dir = tmp_path / "output"
    output_dir.mkdir(exist_ok=True)

    # Create infographic
    img_path = create_infographic(
        csv_path=sample_csv_file,
        output_dir=output_dir,
        title_prefix="Test Infographic",
        figsize=(10, 6),
        dpi=100,
    )

    # Check output path
    expected_path = output_dir / "100_output_infographic.png"
    assert img_path == expected_path
    assert img_path.exists()

    # Basic file size check to ensure the image was created properly
    assert img_path.stat().st_size > 0


def test_create_infographic_default_output_dir(sample_csv_file):
    """Test infographic creation with default output directory."""
    # Create infographic with default output directory (same as CSV)
    img_path = create_infographic(
        csv_path=sample_csv_file,
        output_dir=None,
    )

    # Check output path
    expected_path = sample_csv_file.parent / "100_output_infographic.png"
    assert img_path == expected_path
    assert img_path.exists()

    # Clean up
    os.remove(img_path)


def test_create_infographic_invalid_input(tmp_path):
    """Test handling of invalid input path."""
    output_dir = tmp_path / "output"
    output_dir.mkdir(exist_ok=True)
    non_existent_file = tmp_path / "non_existent.csv"

    with pytest.raises(FileNotFoundError):
        create_infographic(
            csv_path=non_existent_file,
            output_dir=output_dir,
        )
