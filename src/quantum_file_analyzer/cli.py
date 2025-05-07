"""Command-line interface for quantum password analyzer."""

import argparse
import sys
from pathlib import Path
from typing import List, Optional

from quantum_password_analyzer import transform, visualize


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        prog="qpa",
        description="Quantum Password Analyzer - Analyze quantum password cracking timelines",
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Transform command
    transform_parser = subparsers.add_parser(
        "transform", help="Transform password cracking estimates with a speedup factor"
    )
    transform_parser.add_argument(
        "--input",
        "-i",
        type=str,
        default="data/input/input.csv",
        help="Input CSV file with original estimates",
    )
    transform_parser.add_argument(
        "--output-dir",
        "-o",
        type=str,
        default="data/output",
        help="Directory to save output files",
    )
    transform_parser.add_argument(
        "--factor",
        "-f",
        type=float,
        help="Speedup factor to apply (if not provided, will prompt)",
    )
    transform_parser.add_argument(
        "--no-save-old",
        action="store_true",
        help="Don't save the original data",
    )

    # Visualize command
    viz_parser = subparsers.add_parser(
        "visualize", help="Create infographic from transformed data"
    )
    viz_parser.add_argument(
        "--csv",
        "-c",
        type=str,
        help="CSV file to visualize (if not provided, will prompt for selection)",
    )
    viz_parser.add_argument(
        "--output-dir",
        "-o",
        type=str,
        default="data/output",
        help="Directory to save the infographic",
    )
    viz_parser.add_argument(
        "--title",
        "-t",
        type=str,
        default="Quantum Brute-Force Durations",
        help="Title prefix for the infographic",
    )
    viz_parser.add_argument(
        "--dpi",
        type=int,
        default=300,
        help="Resolution of the output image in DPI",
    )
    viz_parser.add_argument(
        "--width",
        type=int,
        default=14,
        help="Width of the figure in inches",
    )
    viz_parser.add_argument(
        "--height",
        type=int,
        default=8,
        help="Height of the figure in inches",
    )

    # Pipeline command (transform + visualize)
    pipeline_parser = subparsers.add_parser(
        "pipeline", help="Run the complete transform and visualize pipeline"
    )
    pipeline_parser.add_argument(
        "--input",
        "-i",
        type=str,
        default="data/input/input.csv",
        help="Input CSV file with original estimates",
    )
    pipeline_parser.add_argument(
        "--output-dir",
        "-o",
        type=str,
        default="data/output",
        help="Directory to save output files",
    )
    pipeline_parser.add_argument(
        "--factor",
        "-f",
        type=float,
        help="Speedup factor to apply (if not provided, will prompt)",
    )
    pipeline_parser.add_argument(
        "--title",
        "-t",
        type=str,
        default="Quantum Brute-Force Durations",
        help="Title prefix for the infographic",
    )
    pipeline_parser.add_argument(
        "--dpi",
        type=int,
        default=300,
        help="Resolution of the output image in DPI",
    )

    # List command
    list_parser = subparsers.add_parser(
        "list", help="List available CSV files for visualization"
    )
    list_parser.add_argument(
        "--output-dir",
        "-o",
        type=str,
        default="data/output",
        help="Directory to check for CSV files",
    )

    return parser.parse_args(args)


def run_transform(args: argparse.Namespace) -> Optional[Path]:
    """Run the transform command."""
    try:
        csv_path, _ = transform.transform_data(
            input_path=args.input,
            output_dir=args.output_dir,
            speedup_factor=(
                args.factor
                if args.factor is not None
                else transform.main(
                    input_path=args.input,
                    output_dir=args.output_dir,
                    speedup_factor=None,
                )[0]
            ),
            save_old=not args.no_save_old,
        )
        return csv_path
    except Exception as e:
        print(f"Error during transformation: {e}", file=sys.stderr)
        return None


def run_visualize(args: argparse.Namespace) -> Optional[Path]:
    """Run the visualize command."""
    try:
        csv_path = args.csv
        if csv_path is None:
            csv_path = visualize.select_csv_file(args.output_dir)
            if csv_path is None:
                return None

        return visualize.create_infographic(
            csv_path=csv_path,
            output_dir=args.output_dir,
            title_prefix=args.title,
            figsize=(args.width, args.height),
            dpi=args.dpi,
        )
    except Exception as e:
        print(f"Error during visualization: {e}", file=sys.stderr)
        return None


def run_pipeline(args: argparse.Namespace) -> Optional[Path]:
    """Run the complete pipeline."""
    try:
        # Transform
        transform_args = argparse.Namespace(
            input=args.input,
            output_dir=args.output_dir,
            factor=args.factor,
            no_save_old=False,
        )
        csv_path = run_transform(transform_args)
        if csv_path is None:
            return None

        # Visualize
        viz_args = argparse.Namespace(
            csv=str(csv_path),
            output_dir=args.output_dir,
            title=args.title,
            dpi=args.dpi,
            width=14,
            height=8,
        )
        return run_visualize(viz_args)
    except Exception as e:
        print(f"Error during pipeline: {e}", file=sys.stderr)
        return None


def list_csv_files(args: argparse.Namespace) -> None:
    """List available CSV files for visualization."""
    output_dir = Path(args.output_dir)
    csv_files = sorted(output_dir.glob("*_output.csv"))

    if not csv_files:
        print(f"No '*_output.csv' files found in {output_dir}")
        return

    print(f"\nFound {len(csv_files)} CSV files in {output_dir}:")
    for i, f in enumerate(csv_files, 1):
        print(f"  [{i}] {f.name}")


def main(args: Optional[List[str]] = None) -> int:
    """Main entry point for the CLI."""
    parsed_args = parse_args(args)

    if not parsed_args.command:
        print("Error: Please specify a command.")
        print("Run 'qpa --help' for usage information.")
        return 1

    if parsed_args.command == "transform":
        result = run_transform(parsed_args)
        return 0 if result else 1

    elif parsed_args.command == "visualize":
        result = run_visualize(parsed_args)
        return 0 if result else 1

    elif parsed_args.command == "pipeline":
        result = run_pipeline(parsed_args)
        return 0 if result else 1

    elif parsed_args.command == "list":
        list_csv_files(parsed_args)
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
