#!/usr/bin/env python3
# File: quantum_infographic.py
"""
Create a heat-map infographic from an optimised brute-force CSV whose
name embeds the optimisation factor: data/output/{factor}_output.csv
"""

from __future__ import annotations

import re
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ── Ask which factor file to render ─────────────────────────────────────────
OUTPUT_DIR = Path("data/output")
csv_files = sorted(OUTPUT_DIR.glob("*_output.csv"))
if not csv_files:
    raise FileNotFoundError("No '*_output.csv' files found in data/output/")

print("\nAvailable optimised CSV files:")
for i, f in enumerate(csv_files, 1):
    print(f"  [{i}] {f.name}")
choice = input("Select file number to plot (blank = 1): ").strip()
idx = 1 if choice == "" else int(choice)
csv_path = csv_files[idx - 1]

# ── Load data ───────────────────────────────────────────────────────────────
df = pd.read_csv(csv_path)
duration_cols = [c for c in df.columns if c != "Number of Characters"]

# ── Convert durations to seconds for colour scale ───────────────────────────
_SEC_PER_UNIT = {
    "second": 1,
    "minute": 60,
    "hour": 3600,
    "day": 86_400,
    "week": 604_800,
    "month": 2_592_000,
    "year": 31_557_600,
}
_PREFIX_MULT = {
    "": 1,
    "k": 1e3,
    "m": 1e6,
    "bn": 1e9,
    "tn": 1e12,
    "qd": 1e15,
    "qn": 1e15,
}
_pat = re.compile(
    r"(?P<num>\d+(?:\.\d+)?)\s*(?P<pref>[a-zA-Z]{0,2})\s*"
    r"(?P<unit>seconds?|minutes?|hours?|days?|weeks?|months?|years?)"
)


def to_sec(txt: str) -> float:
    if txt.lower() == "instantly":
        return 0.5
    m = _pat.fullmatch(txt.strip())
    return (
        float(m.group("num"))
        * _PREFIX_MULT[m.group("pref").lower()]
        * _SEC_PER_UNIT[m.group("unit").rstrip("s")]
    )


sec = df[duration_cols].applymap(to_sec).to_numpy()

# ── Plot heat-map ───────────────────────────────────────────────────────────
plt.figure(figsize=(14, 8))
norm = plt.cm.colors.LogNorm(vmin=sec.min(), vmax=sec.max())
im = plt.imshow(sec, cmap="viridis_r", norm=norm)

plt.xticks(np.arange(len(duration_cols)), duration_cols, rotation=35, ha="right")
plt.yticks(np.arange(len(df)), df["Number of Characters"])
for i in range(sec.shape[0]):
    for j in range(sec.shape[1]):
        plt.text(
            j, i, df.iloc[i, j + 1], ha="center", va="center", color="white", fontsize=8
        )
plt.colorbar(im, label="Seconds (log scale)")
plt.title(f"Quantum Brute-Force Durations (Optimised ×{csv_path.stem.split('_')[0]})")
plt.tight_layout()

out_img = OUTPUT_DIR / f"{csv_path.stem}_infographic.png"
plt.savefig(out_img, dpi=300)
print(f"\n✓ Infographic saved → {out_img}")