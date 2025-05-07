"""
Transform a first-round quantum brute-force table stored in
Quantum_Data__O_SQRT_N.csv (“old”) into a more-optimistic projection (“optimized”).

Steps
1. Read the CSV file (edit INPUT_CSV if the name or path differs).
2. Convert every duration string to seconds.
3. Divide by SPEEDUP_FACTOR to simulate a faster quantum computer.
4. Re-format seconds back into a compact text representation.
5. Write   password_bruteforce_old.csv   and   password_bruteforce_optimized.csv.

Assumptions
* Column layout matches the earlier table:
  ── “Number of Characters” plus five complexity columns
    (“Numbers Only”, “Lowercase Letters”, … “Numbers, Upper and Lowercase Letters, Symbols”)
* The duration strings follow the same patterns
    (e.g., “Instantly”, “1.4 hours”, “4.2k years”, “1.4bn years”)
"""

from __future__ import annotations

import math
import re
from pathlib import Path

import pandas as pd

# ──────────────────────────────────────────────────────────────────────────────
# 1.  Configuration
# ──────────────────────────────────────────────────────────────────────────────
INPUT_CSV = Path("Quantum_Data__O_SQRT_N.csv")
SPEEDUP_FACTOR = 100  # Optimistic improvement: 100× faster than “old”

# ──────────────────────────────────────────────────────────────────────────────
# 2.  Helpers for time-string ⇄ seconds conversions
# ──────────────────────────────────────────────────────────────────────────────
_SEC_PER_UNIT = {
    "second": 1,
    "minute": 60,
    "hour": 3600,
    "day": 86400,
    "week": 604800,
    "month": 30 * 86400,  # 30-day months
    "year": 365.25 * 86400,  # Julian year
}
_PREFIX_MULT = {  # magnitude prefixes
    "": 1,
    "k": 1e3,
    "m": 1e6,
    "bn": 1e9,
    "tn": 1e12,
    "qd": 1e15,
    "qn": 1e15,
}

_DURATION_RE = re.compile(
    r"""
    (?P<num>\d+(?:\.\d+)?)            # number
    \s*
    (?P<prefix>[a-zA-Z]{0,2})         # optional k, m, bn, …
    \s*
    (?P<unit>seconds?|minutes?|hours?|days?|weeks?|months?|years?)  # unit
    """,
    re.VERBOSE,
)


def text_to_seconds(txt: str) -> float:
    """Convert human-readable duration to seconds.  'Instantly' → 0."""
    if txt.strip().lower() == "instantly":
        return 0.0
    m = _DURATION_RE.fullmatch(txt.strip())
    if not m:
        raise ValueError(f"Unrecognized duration: {txt!r}")
    value = float(m.group("num"))
    prefix = m.group("prefix").lower()
    unit = m.group("unit").rstrip("s")  # singular
    seconds = value * _PREFIX_MULT[prefix] * _SEC_PER_UNIT[unit]
    return seconds


def seconds_to_text(seconds: float) -> str:
    """Convert seconds into a compact description resembling the source style."""
    if seconds < 0.5:
        return "Instantly"

    # pick the most intuitive unit
    for unit, sec_per in reversed(list(_SEC_PER_UNIT.items())):
        if seconds >= sec_per:
            value = seconds / sec_per
            break

    # insert magnitude prefix if value still huge
    for prefix, mult in reversed(list(_PREFIX_MULT.items())):
        adj = value / mult
        if 1 <= adj < 1000:
            value, chosen_prefix = adj, prefix
            break
    else:
        chosen_prefix = ""

    value_str = (
        str(int(value))
        if value.is_integer()
        else f"{value:.1f}".rstrip("0").rstrip(".")
    )
    unit += "s" if value != 1 else ""
    space = " " if chosen_prefix == "" else ""
    return f"{value_str}{chosen_prefix}{space}{unit}"


# ──────────────────────────────────────────────────────────────────────────────
# 3.  Load the CSV
# ──────────────────────────────────────────────────────────────────────────────
if not INPUT_CSV.exists():
    raise FileNotFoundError(f"Input file not found: {INPUT_CSV}")

df_old = pd.read_csv(INPUT_CSV)

# Ensure expected structure
expected_cols = [
    "Number of Characters",
    "Numbers Only",
    "Lowercase Letters",
    "Upper and Lowercase Letters",
    "Numbers, Upper and Lowercase Letters",
    "Numbers, Upper and Lowercase Letters, Symbols",
]
missing = [c for c in expected_cols if c not in df_old.columns]
if missing:
    raise ValueError(f"CSV missing expected columns: {missing}")

duration_cols = expected_cols[1:]

# ──────────────────────────────────────────────────────────────────────────────
# 4.  Convert strings → seconds,  apply speed-up,  seconds → strings
# ──────────────────────────────────────────────────────────────────────────────
df_opt = df_old.copy()

for col in duration_cols:
    seconds = df_old[col].map(text_to_seconds)
    df_old[col + " (s)"] = seconds  # keep a numeric backup
    new_seconds = seconds / SPEEDUP_FACTOR
    df_opt[col] = new_seconds.map(seconds_to_text)
    df_opt[col + " (s)"] = new_seconds

# ──────────────────────────────────────────────────────────────────────────────
# 5.  Export old + optimized tables
# ──────────────────────────────────────────────────────────────────────────────
OUT_OLD = Path("password_bruteforce_old.csv")
OUT_OPT = Path("password_bruteforce_optimized.csv")

df_old[expected_cols].to_csv(OUT_OLD, index=False)
df_opt[expected_cols].to_csv(OUT_OPT, index=False)

print(f"✓ Wrote {OUT_OLD}")
print(f"✓ Wrote {OUT_OPT}")
print(f"  Speed-up factor applied: {SPEEDUP_FACTOR}×")
