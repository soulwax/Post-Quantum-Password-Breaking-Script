# Quantum Password Analyzer

A Python package for analyzing quantum password cracking timelines and creating visual infographics.

## Overview

Quantum Password Analyzer is a tool that helps visualize the impact of quantum computing on password security. It transforms password-cracking time estimates and creates heat-map infographics to show how long it would take quantum computers to brute-force passwords of different lengths and complexities.

## Features

- **Transform Data**: Apply speedup factors to baseline quantum computing password cracking estimates
- **Visualize Results**: Generate heat-map infographics showing the time required to crack passwords
- **Simple CLI**: Command-line interface for easy usage
- **Python API**: Use as a library in your own projects

## Installation

### From PyPI

```bash
pip install quantum-password-analyzer
```

### From Source

```bash
git clone https://github.com/yourusername/quantum-password-analyzer.git
cd quantum-password-analyzer
pip install -e .
```

## Usage

### Command Line Interface

The package provides a command-line tool `qpa` with several subcommands:

#### Transform Data

```bash
# Transform with interactive factor input
qpa transform --input data/input/input.csv --output-dir data/output

# Transform with specific factor
qpa transform --input data/input/input.csv --output-dir data/output --factor 500
```

#### Visualize Data

```bash
# Select file interactively
qpa visualize --output-dir data/output

# Visualize specific file
qpa visualize --csv data/output/500_output.csv --title "My Custom Title"
```

#### Run Complete Pipeline

```bash
# Run transform and visualize in one step
qpa pipeline --input data/input/input.csv --output-dir data/output --factor 500
```

#### List Available Files

```bash
qpa list --output-dir data/output
```

### Python API

```python
from quantum_password_analyzer import transform_data, create_infographic

# Transform data with a speedup factor
output_csv, _ = transform_data(
    input_path="data/input/input.csv",
    output_dir="data/output",
    speedup_factor=500
)

# Create an infographic
infographic_path = create_infographic(
    csv_path=output_csv,
    output_dir="data/output",
    title_prefix="Quantum Brute-Force Times"
)

print(f"Infographic created: {infographic_path}")
```

## Input Data Format

The input CSV should have the following format:

- First column: "Number of Characters" (password length)
- Additional columns: Different password complexity categories (e.g., "Numbers Only", "Lowercase Letters", etc.)
- Cell values: Human-readable time durations (e.g., "5 seconds", "10 minutes", "2 hours", "1 day", "3 weeks", "5 months", "2 years")

Example:

```csv
Number of Characters,Numbers Only,Lowercase Letters,Upper and Lowercase Letters,Numbers + Upper and Lowercase,Numbers + Upper and Lowercase + Symbols
4,Instantly,1 second,5 seconds,1 minute,10 minutes
6,1 second,1 minute,1 hour,1 day,1 week
8,2 minutes,1 day,1 year,10 years,100 years
```

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/quantum-password-analyzer.git
cd quantum-password-analyzer

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or .\venv\Scripts\activate  # Windows

# Install development dependencies
pip install -e ".[dev]"
```

### Run Tests

```bash
pytest
```

### Code Formatting

```bash
# Format code with Black
black src tests

# Check code with Ruff
ruff check src tests
```

## Project Structure

```
quantum-password-analyzer/
├── src/
│   └── quantum_password_analyzer/
│       ├── __init__.py         # Package exports
│       ├── transform.py        # Data transformation functions
│       ├── visualize.py        # Visualization functions
│       ├── utils.py            # Common utilities
│       └── cli.py              # Command-line interface
├── tests/                      # Test suite
├── data/                       # Sample data
│   ├── input/                  # Input CSV files
│   └── output/                 # Generated outputs
├── pyproject.toml              # Package configuration
├── README.md                   # This file
└── LICENSE                     # License file
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the GPL-3.0 License - see the [LICENSE](LICENSE) file for details.
