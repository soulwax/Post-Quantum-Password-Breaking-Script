"""Transform quantum brute-force estimates."""

from __future__ import annotations

from pathlib import Path
from typing import Optional, Union

import pandas as pd
from quantum_password_analyzer.utils import (
    ensure_dir,
    factor_str,
    seconds_to_text,
    text_to_seconds,
)


def transform_data(
    input_path: Union[str, Path],
    output_dir: Union[str, Path],
    speedup_factor: float = 100,
    save_old: bool = True,
) -> tuple[Path, Optional[Path]]:
    """Transform quantum password cracking time estimates by a speedup factor.

    Args:
        input_path: Path to input CSV file
        output_dir: Directory to save output CSV files
        speedup_factor: Factor by which to divide the durations
        save_old: Whether to save the original data as well

    Returns:
        Tuple of (optimized_csv_path, original_csv_path or None)
    """
    # Validate input
    input_path = Path(input_path)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    output_dir = ensure_dir(output_dir)

    # Load data
    df_old = pd.read_csv(input_path)
    duration_cols = [c for c in df_old.columns if c != "Number of Characters"]

    # Apply transformation
    df_opt = df_old.copy()
    for col in duration_cols:
        secs = df_old[col].map(text_to_seconds)
        df_opt[col] = (secs / speedup_factor).map(seconds_to_text)

    # Prepare output paths and save files
    opt_name = f"{factor_str(speedup_factor)}_output.csv"
    opt_path = output_dir / opt_name

    # Save optimized data
    df_opt[["Number of Characters"] + duration_cols].to_csv(opt_path, index=False)

    # Save original data if requested
    old_path = None
    if save_old:
        old_path = output_dir / "password_bruteforce_old.csv"
        df_old[["Number of Characters"] + duration_cols].to_csv(old_path, index=False)

    return opt_path, old_path


def main(
    input_path: str = "data/input/input.csv",
    output_dir: str = "data/output",
    speedup_factor: Optional[float] = None,
    min_factor: float = 1,
    max_factor: float = 1_000_000,
    default_factor: float = 100,
) -> tuple[Path, Optional[Path]]:
    """Run the transformation with interactive factor input if needed.

    Args:
        input_path: Path to the input CSV
        output_dir: Directory to save outputs
        speedup_factor: Optimization factor (if None, will prompt user)
        min_factor: Minimum allowed factor
        max_factor: Maximum allowed factor
        default_factor: Default factor when user provides blank input

    Returns:
        Tuple of (optimized_csv_path, original_csv_path or None)
    """
    # Interactive mode if no factor provided
    if speedup_factor is None:
        prompt = (
            f"Enter optimisation speed-up factor "
            f"({min_factor}–{max_factor}, blank = {default_factor}): "
        )
        while True:
            ans = input(prompt).strip()
            if not ans:
                speedup_factor = default_factor
                break
            try:
                val = float(ans)
            except ValueError:
                print("  ✖  Number required.")
                continue
            if min_factor <= val <= max_factor:
                speedup_factor = val
                break
            print(f"  ✖  Enter a value between {min_factor} and {max_factor}.")

    # Process and save data
    opt_path, old_path = transform_data(input_path, output_dir, speedup_factor)

    # Print success message
    print(f"\n✓ Speed-up factor applied: {speedup_factor}×")
    if old_path:
        print(f"✓ Wrote {old_path}")
    print(f"✓ Wrote {opt_path}")

    return opt_path, old_path


if __name__ == "__main__":
    main()
