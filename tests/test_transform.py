"""Tests for data transformation functions."""

import io
import os
from pathlib import Path

import pandas as pd
import pytest
from quantum_password_analyzer.transform import transform_data


@pytest.fixture
def sample_input_csv(tmp_path):
    """Create a sample input CSV file for testing."""
    input_path = tmp_path / "input.csv"
    sample_data = """Number of Characters,Numbers Only,Lowercase Letters,Upper and Lowercase Letters
4,Instantly,1 second,5 seconds
6,1 second,1 minute,1 hour
8,2 minutes,1 day,1 year
"""
    input_path.write_text(sample_data)
    return input_path


def test_transform_data(sample_input_csv, tmp_path):
    """Test data transformation with specified factor."""
    output_dir = tmp_path / "output"

    # Test with factor 100
    opt_path, old_path = transform_data(
        input_path=sample_input_csv,
        output_dir=output_dir,
        speedup_factor=100,
        save_old=True,
    )

    # Check output paths
    assert opt_path == output_dir / "100_output.csv"
    assert old_path == output_dir / "password_bruteforce_old.csv"
    assert opt_path.exists()
    assert old_path.exists()

    # Check original data
    df_old = pd.read_csv(old_path)
    assert list(df_old.columns) == [
        "Number of Characters",
        "Numbers Only",
        "Lowercase Letters",
        "Upper and Lowercase Letters",
    ]
    assert df_old.loc[0, "Numbers Only"] == "Instantly"
    assert df_old.loc[1, "Lowercase Letters"] == "1 minute"
    assert df_old.loc[2, "Upper and Lowercase Letters"] == "1 year"

    # Check optimized data (100x faster)
    df_opt = pd.read_csv(opt_path)
    assert list(df_opt.columns) == list(df_old.columns)
    assert df_opt.loc[0, "Numbers Only"] == "Instantly"  # Already at minimum
    assert df_opt.loc[1, "Lowercase Letters"] == "0.6 seconds"  # 60 seconds / 100
    assert df_opt.loc[2, "Upper and Lowercase Letters"] == "3.7 days"  # 1 year / 100


def test_transform_data_no_save_old(sample_input_csv, tmp_path):
    """Test data transformation without saving original data."""
    output_dir = tmp_path / "output"

    # Test with save_old=False
    opt_path, old_path = transform_data(
        input_path=sample_input_csv,
        output_dir=output_dir,
        speedup_factor=10,
        save_old=False,
    )

    # Check output paths
    assert opt_path == output_dir / "10_output.csv"
    assert old_path is None
    assert opt_path.exists()
    assert not (output_dir / "password_bruteforce_old.csv").exists()


def test_transform_data_invalid_input(tmp_path):
    """Test handling of invalid input path."""
    output_dir = tmp_path / "output"
    non_existent_file = tmp_path / "non_existent.csv"

    with pytest.raises(FileNotFoundError):
        transform_data(
            input_path=non_existent_file,
            output_dir=output_dir,
            speedup_factor=100,
        )
