#!/usr/bin/env python3
# File: conversion.py
"""
Convert first-round quantum brute-force estimates (“old”) into an
optimised projection (“optimised”) and save the result in
data/output/{factor}_output.csv.

Input  : data/input/input.csv
Outputs: data/output/password_bruteforce_old.csv
         data/output/{factor}_output.csv
"""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

# ── Paths ────────────────────────────────────────────────────────────────────
INPUT_CSV = Path("data/input/input.csv")
OUTPUT_DIR = Path("data/output")

# ── Factor bounds + default ─────────────────────────────────────────────────
DEFAULT_FACTOR = 100  # blank entry ⇒ 100 × faster
MIN_FACTOR = 1
MAX_FACTOR = 1_000_000


def ask_speedup() -> float:
    prompt = (
        f"Enter optimisation speed-up factor "
        f"({MIN_FACTOR}–{MAX_FACTOR}, blank = {DEFAULT_FACTOR}): "
    )
    while True:
        ans = input(prompt).strip()
        if not ans:
            return DEFAULT_FACTOR
        try:
            val = float(ans)
        except ValueError:
            print("  ✖  Number required.")
            continue
        if MIN_FACTOR <= val <= MAX_FACTOR:
            return val
        print(f"  ✖  Enter a value between {MIN_FACTOR} and {MAX_FACTOR}.")


SPEEDUP_FACTOR = ask_speedup()

# ── Utility: text ⇄ seconds ─────────────────────────────────────────────────
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

_dur_re = re.compile(
    r"(?P<num>\d+(?:\.\d+)?)\s*"
    r"(?P<prefix>[a-zA-Z]{0,2})\s*"
    r"(?P<unit>seconds?|minutes?|hours?|days?|weeks?|months?|years?)$"
)


def text_to_seconds(txt: str) -> float:
    if txt.lower() == "instantly":
        return 0.0
    m = _dur_re.fullmatch(txt.strip())
    val = float(m.group("num"))
    prefix = _PREFIX_MULT[m.group("prefix").lower()]
    unit = _SEC_PER_UNIT[m.group("unit").rstrip("s")]
    return val * prefix * unit


def seconds_to_text(sec: float) -> str:
    if sec < 0.5:
        return "Instantly"
    for unit, s_per in reversed(_SEC_PER_UNIT.items()):
        if sec >= s_per:
            val = sec / s_per
            break
    for pref, mult in reversed(_PREFIX_MULT.items()):
        adj = val / mult
        if 1 <= adj < 1000:
            val, chosen = adj, pref
            break
    else:
        chosen = ""
    val_str = (
        f"{int(val)}" if val.is_integer() else f"{val:.1f}".rstrip("0").rstrip(".")
    )
    unit += "s" if val != 1 else ""
    space = " " if chosen == "" else ""
    return f"{val_str}{chosen}{space}{unit}"


# ── Load CSV ────────────────────────────────────────────────────────────────
if not INPUT_CSV.exists():
    raise FileNotFoundError(INPUT_CSV)
df_old = pd.read_csv(INPUT_CSV)
duration_cols = [c for c in df_old.columns if c != "Number of Characters"]

# ── Build optimised table ───────────────────────────────────────────────────
df_opt = df_old.copy()
for col in duration_cols:
    secs = df_old[col].map(text_to_seconds)
    df_opt[col] = (secs / SPEEDUP_FACTOR).map(seconds_to_text)

# ── Write outputs ───────────────────────────────────────────────────────────
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# unchanged first-round figures
(df_old[["Number of Characters"] + duration_cols]).to_csv(
    OUTPUT_DIR / "password_bruteforce_old.csv", index=False
)


# optimised figures – filename embeds factor
def factor_str(f: float) -> str:
    return str(int(f)) if f.is_integer() else str(f).replace(".", "_")


opt_name = f"{factor_str(SPEEDUP_FACTOR)}_output.csv"
(df_opt[["Number of Characters"] + duration_cols]).to_csv(
    OUTPUT_DIR / opt_name, index=False
)

print(f"\n✓ Speed-up factor applied: {SPEEDUP_FACTOR}×")
print(f"✓ Wrote {OUTPUT_DIR/'password_bruteforce_old.csv'}")
print(f"✓ Wrote {OUTPUT_DIR/opt_name}")