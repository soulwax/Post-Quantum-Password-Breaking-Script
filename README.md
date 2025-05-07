# Quantum Password Cracking Infographic

## Overview

This project generates an infographic from a CSV file containing quantum password-cracking estimates. It allows you to visualize the impact of quantum computing on password security by transforming the data and creating a heat-map infographic.
The infographic shows the time it would take to brute-force a password of a given length and complexity using quantum computing, compared to classical methods.

## Project Structure / Files

```plaintext
.
├── data
│   ├── input
│   │   └── input.csv          # first-round quantum-estimates table
│   └── output/                # generated CSVs + infographics
├── quantum_transform.py       # converts table with chosen speed-up
└── quantum_infographic.py     # renders heat-map from an optimised CSV
```

---

## 1  Set up a virtual environment

```bash
python -m venv venv          # create
source venv/bin/activate     # Linux/macOS
# .\venv\Scripts\activate     # Windows PowerShell
```

Creating an isolated **venv** keeps project-specific packages separate. ([Python documentation](https://docs.python.org/3/library/venv.html?utm_source=chatgpt.com), [Python documentation](https://docs.python.org/3/tutorial/venv.html?utm_source=chatgpt.com))

### Install dependencies

```bash
pip install pandas numpy matplotlib  # add any extras you need
```

If you prefer a `requirements.txt`, list those packages and run:

```bash
pip install -r requirements.txt :contentReference[oaicite:1]{index=1}  
```

---

## 2  Transform the data

```bash
python quantum_transform.py
```

You’ll be prompted for an **optimisation speed-up factor** (realistic range 1 – 1 000 000, default 100).
The script reads `data/input/input.csv` and writes two files in `data/output/`:

* `password_bruteforce_old.csv`   – unchanged first-round quantum numbers
* `{factor}_output.csv`           – durations divided by your factor

Example: entering `250` produces `data/output/250_output.csv`.

---

## 3  Generate an infographic

```bash
python quantum_infographic.py
```

The program lists all `*_output.csv` files in `data/output/`; pick one to plot.
Output: `data/output/{factor}_output_infographic.png` – a log-scaled heat-map annotated with the human-readable durations.

---

## 4  Typical workflow

```bash
# 1 create / activate venv (once)
python -m venv venv
source venv/bin/activate
pip install pandas numpy matplotlib

# 2 run converter (each factor you want)
python quantum_transform.py      # enter, e.g., 500

# 3 make graphic
python quantum_infographic.py    # choose 500_output.csv

# 4 open PNG in your favourite viewer
```

---

## 5  Extending

* **Batch processing** – loop through multiple factors and call both scripts automatically.
* **CLI options** – integrate `argparse` or `click` to accept `--factor` and `--input` flags.
* **Integrity checks** – compute a SHA-256 hash of each CSV and store it alongside the file for tamper detection.
* **Unit tests** – use `unittest` or `pytest` to validate the transformation logic and plotting functions.
* **Documentation** – add docstrings to functions and classes, and consider using Sphinx for generating HTML documentation.
* **Logging** – implement logging to track the execution flow and errors, using Python's built-in `logging` module.
* **Configuration files** – use a configuration file (e.g., JSON or YAML) to store parameters like the input file path, output directory, and speed-up factor. This makes it easier to change settings without modifying the code.
* **Error handling** – add try-except blocks to handle potential errors, such as file not found or invalid data formats.
* **Code formatting** – use a code formatter like `black` or `autopep8` to ensure consistent code style.
* **Type hints** – add type hints to function signatures to improve code readability and help with static type checking.
