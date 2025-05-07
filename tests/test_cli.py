"""Tests for CLI functions."""

from pathlib import Path
from unittest.mock import patch

import pytest
from quantum_password_analyzer.cli import main, parse_args


def test_parse_args():
    """Test argument parsing."""
    # Test transform command
    args = parse_args(["transform", "--input", "my_file.csv", "--factor", "200"])
    assert args.command == "transform"
    assert args.input == "my_file.csv"
    assert args.factor == 200

    # Test visualize command
    args = parse_args(["visualize", "--csv", "output.csv", "--dpi", "150"])
    assert args.command == "visualize"
    assert args.csv == "output.csv"
    assert args.dpi == 150

    # Test pipeline command
    args = parse_args(["pipeline", "--factor", "500", "--title", "Custom Title"])
    assert args.command == "pipeline"
    assert args.factor == 500
    assert args.title == "Custom Title"

    # Test list command
    args = parse_args(["list", "--output-dir", "custom/path"])
    assert args.command == "list"
    assert args.output_dir == "custom/path"


@patch("quantum_password_analyzer.cli.transform.transform_data")
def test_run_transform(mock_transform, tmp_path):
    """Test running the transform command."""
    # Setup mock return value
    csv_path = tmp_path / "result.csv"
    mock_transform.return_value = (csv_path, None)

    # Run CLI with transform command
    exit_code = main(
        [
            "transform",
            "--input",
            "test.csv",
            "--factor",
            "200",
            "--output-dir",
            str(tmp_path),
            "--no-save-old",
        ]
    )

    # Check mock was called with correct arguments
    mock_transform.assert_called_once()
    args = mock_transform.call_args[1]
    assert args["input_path"] == "test.csv"
    assert args["output_dir"] == str(tmp_path)
    assert args["speedup_factor"] == 200
    assert args["save_old"] is False

    # Check exit code
    assert exit_code == 0


@patch("quantum_password_analyzer.cli.visualize.create_infographic")
def test_run_visualize(mock_visualize, tmp_path):
    """Test running the visualize command."""
    # Setup mock return value
    img_path = tmp_path / "infographic.png"
    mock_visualize.return_value = img_path

    # Run CLI with visualize command
    exit_code = main(
        [
            "visualize",
            "--csv",
            "test.csv",
            "--output-dir",
            str(tmp_path),
            "--title",
            "Test Title",
            "--dpi",
            "150",
            "--width",
            "12",
            "--height",
            "10",
        ]
    )

    # Check mock was called with correct arguments
    mock_visualize.assert_called_once()
    args = mock_visualize.call_args[1]
    assert args["csv_path"] == "test.csv"
    assert args["output_dir"] == str(tmp_path)
    assert args["title_prefix"] == "Test Title"
    assert args["dpi"] == 150
    assert args["figsize"] == (12, 10)

    # Check exit code
    assert exit_code == 0


@patch("quantum_password_analyzer.cli.run_transform")
@patch("quantum_password_analyzer.cli.run_visualize")
def test_run_pipeline(mock_visualize, mock_transform, tmp_path):
    """Test running the pipeline command."""
    # Setup mock returns
    csv_path = tmp_path / "result.csv"
    img_path = tmp_path / "infographic.png"
    mock_transform.return_value = csv_path
    mock_visualize.return_value = img_path

    # Run CLI with pipeline command
    exit_code = main(
        [
            "pipeline",
            "--input",
            "test.csv",
            "--output-dir",
            str(tmp_path),
            "--factor",
            "300",
            "--title",
            "Pipeline Test",
        ]
    )

    # Check exit code
    assert exit_code == 0

    # Check transform was called
    mock_transform.assert_called_once()

    # Check visualize was called with csv_path from transform
    mock_visualize.assert_called_once()


@patch("quantum_password_analyzer.cli.list_csv_files")
def test_run_list(mock_list, tmp_path):
    """Test running the list command."""
    # Run CLI with list command
    exit_code = main(["list", "--output-dir", str(tmp_path)])

    # Check mock was called with correct arguments
    mock_list.assert_called_once()
    args = mock_list.call_args[0][0]
    assert args.output_dir == str(tmp_path)

    # Check exit code
    assert exit_code == 0


def test_no_command():
    """Test running without a command."""
    with patch("sys.stdout") as mock_stdout:
        exit_code = main([])
        assert exit_code == 1
