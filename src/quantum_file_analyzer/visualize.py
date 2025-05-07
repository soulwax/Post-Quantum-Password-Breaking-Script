"""Create infographics from quantum password cracking data."""

from __future__ import annotations

import re
from pathlib import Path
from typing import List, Optional, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from quantum_password_analyzer.utils import ensure_dir, text_to_seconds


def create_infographic(
    csv_path: Union[str, Path],
    output_dir: Optional[Union[str, Path]] = None,
    title_prefix: str = "Quantum Brute-Force Durations",
    figsize: Tuple[int, int] = (14, 8),
    dpi: int = 300,
) -> Path:
    """Create a heat-map infographic from quantum password cracking data.

    Args:
        csv_path: Path to CSV file with password cracking durations
        output_dir: Directory to save the output image (defaults to same as CSV)
        title_prefix: Prefix for the plot title
        figsize: Figure size (width, height) in inches
        dpi: Resolution in dots per inch

    Returns:
        Path to the saved infographic image
    """
    # Handle paths
    csv_path = Path(csv_path)
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    if output_dir is None:
        output_dir = csv_path.parent
    else:
        output_dir = ensure_dir(output_dir)

    # Load data
    df = pd.read_csv(csv_path)
    duration_cols = [c for c in df.columns if c != "Number of Characters"]

    # Convert durations to seconds for color scale
    sec = df[duration_cols].applymap(text_to_seconds).to_numpy()

    # Extract optimization factor from filename if available
    factor_match = re.search(r"^(\d+(?:[._]\d+)?)_", csv_path.stem)
    factor_text = ""
    if factor_match:
        factor = factor_match.group(1).replace("_", ".")
        factor_text = f" (Optimised ×{factor})"

    # Create figure
    plt.figure(figsize=figsize)
    norm = plt.cm.colors.LogNorm(vmin=max(0.01, sec.min()), vmax=sec.max())
    im = plt.imshow(sec, cmap="viridis_r", norm=norm)

    # Add labels and annotations
    plt.xticks(np.arange(len(duration_cols)), duration_cols, rotation=35, ha="right")
    plt.yticks(np.arange(len(df)), df["Number of Characters"])

    for i in range(sec.shape[0]):
        for j in range(sec.shape[1]):
            plt.text(
                j,
                i,
                df.iloc[i, j + 1],
                ha="center",
                va="center",
                color="white",
                fontsize=8,
            )

    plt.colorbar(im, label="Seconds (log scale)")
    plt.title(f"{title_prefix}{factor_text}")
    plt.tight_layout()

    # Save figure
    out_img = output_dir / f"{csv_path.stem}_infographic.png"
    plt.savefig(out_img, dpi=dpi)

    return out_img


def select_csv_file(
    output_dir: Union[str, Path] = "data/output",
) -> Optional[Path]:
    """Interactive selection of CSV file from output directory.

    Args:
        output_dir: Directory containing the CSV files

    Returns:
        Path to the selected CSV file or None if cancelled
    """
    output_dir = Path(output_dir)
    csv_files = sorted(output_dir.glob("*_output.csv"))

    if not csv_files:
        print(f"No '*_output.csv' files found in {output_dir}")
        return None

    print("\nAvailable optimised CSV files:")
    for i, f in enumerate(csv_files, 1):
        print(f"  [{i}] {f.name}")

    choice = input("Select file number to plot (blank = 1, 0 = cancel): ").strip()

    if choice == "0":
        return None

    idx = 1 if choice == "" else int(choice)
    if idx < 1 or idx > len(csv_files):
        print(f"Invalid selection. Please choose 1-{len(csv_files)}")
        return None

    return csv_files[idx - 1]


def main(
    csv_path: Optional[Union[str, Path]] = None,
    output_dir: str = "data/output",
) -> Optional[Path]:
    """Run the visualization with interactive file selection if needed.

    Args:
        csv_path: Path to the CSV file (if None, will prompt user)
        output_dir: Directory to look for CSV files and save output

    Returns:
        Path to the generated infographic or None if cancelled
    """
    # Get CSV path interactively if not provided
    if csv_path is None:
        csv_path = select_csv_file(output_dir)
        if csv_path is None:
            return None

    # Create and save the infographic
    infographic_path = create_infographic(csv_path, output_dir)
    print(f"\n✓ Infographic saved → {infographic_path}")

    return infographic_path


if __name__ == "__main__":
    main()
