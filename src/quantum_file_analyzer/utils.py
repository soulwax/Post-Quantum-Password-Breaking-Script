"""Utility functions for quantum password analyzer."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, Tuple, Union

# Time conversion constants
SEC_PER_UNIT = {
    "second": 1,
    "minute": 60,
    "hour": 3600,
    "day": 86_400,
    "week": 604_800,
    "month": 2_592_000,
    "year": 31_557_600,
}

PREFIX_MULT = {
    "": 1,
    "k": 1e3,
    "m": 1e6,
    "bn": 1e9,
    "tn": 1e12,
    "qd": 1e15,
    "qn": 1e15,
}

# Regular expression pattern for parsing duration strings
DURATION_PATTERN = re.compile(
    r"(?P<num>\d+(?:\.\d+)?)\s*"
    r"(?P<prefix>[a-zA-Z]{0,2})\s*"
    r"(?P<unit>seconds?|minutes?|hours?|days?|weeks?|months?|years?)$"
)


def ensure_dir(path: Union[str, Path]) -> Path:
    """Ensure directory exists."""
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def text_to_seconds(txt: str) -> float:
    """Convert a human-readable duration text to seconds."""
    if txt.lower() == "instantly":
        return 0.0
    m = DURATION_PATTERN.fullmatch(txt.strip())
    if not m:
        raise ValueError(f"Invalid duration format: {txt}")

    val = float(m.group("num"))
    prefix = m.group("prefix").lower()
    unit = m.group("unit").rstrip("s")

    prefix_multiplier = PREFIX_MULT.get(prefix, 1)
    unit_seconds = SEC_PER_UNIT.get(unit)

    if unit_seconds is None:
        raise ValueError(f"Unknown time unit: {unit}")

    return val * prefix_multiplier * unit_seconds


def seconds_to_text(sec: float) -> str:
    """Convert seconds to a human-readable duration text."""
    if sec < 0.5:
        return "Instantly"

    # Find appropriate unit
    for unit, s_per in reversed(list(SEC_PER_UNIT.items())):
        if sec >= s_per:
            val = sec / s_per
            break
    else:
        unit, val = "second", sec

    # Find appropriate prefix
    for pref, mult in reversed(list(PREFIX_MULT.items())):
        adj = val / mult
        if 1 <= adj < 1000:
            val, chosen = adj, pref
            break
    else:
        chosen = ""

    # Format value and unit
    val_str = (
        f"{int(val)}" if val.is_integer() else f"{val:.1f}".rstrip("0").rstrip(".")
    )
    unit_str = f"{unit}s" if val != 1 else unit
    space = " " if chosen == "" else ""

    return f"{val_str}{chosen}{space}{unit_str}"


def factor_str(f: float) -> str:
    """Convert a factor to a string suitable for filenames."""
    return str(int(f)) if f.is_integer() else str(f).replace(".", "_")
