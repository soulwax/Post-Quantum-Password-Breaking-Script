# Post-Quantum-Password-Breaking-Script

## Prerequisites

- Python 3.6 or higher
- pip (Python package installer)
- A virtual environment (optional but recommended, further instructions below)

Execute:

    ```bash
    git clone https://github.com/soulwax/Post-Quantum-Password-Breaking-Script
    ```

## How it works

The script `conversion.py` is a Python script that converts a list of types of
passwords into a more optimized quantum-computer breaking format.

So far it only takes the file, asks the user the optimization rate, then prints the new times to a new csv file.

## Explanation of the code

The code thus far works with the data/input/input.csv file,
which is a CSV file containing the time it takes to break
a password of length N with a quantum computer of runtuime O(sqrt(N)) currently.
The output is in the form of a CSV file with the same format as the input file,
but with the time values multiplied by a user-defined optimization rate within `data/output/outimized.csv`.

## Usage with venv

1. Create a virtual environment (if you haven't already):

    ```bash
    python -m venv venv
    ```

2. Activate the virtual environment:
    - On Windows:

      ```bash
      venv\Scripts\activate
      ```

    - On macOS/Linux:

      ```bash
      source venv/bin/activate
      ```

3. On vscode, make sure to select the correct interpreter for the virtual environment. You can do this by pressing `Ctrl + Shift + P` (or `Cmd + Shift + P` on macOS) and typing "Python: Select Interpreter". Choose the one that points to your virtual environment.

4. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

5. Run the script:

    ```bash
    python conversion.py
    ```
