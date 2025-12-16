# SQShield: SQL Injection Detection Tool

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![PyPI Version](https://img.shields.io/pypi/v/sqshield.svg)

SQShield is a tool to detect potential SQL injection (SQLi) attacks. It provides both a command-line interface and a Python API to classify queries as either malicious or benign, helping you secure your applications against common database threats.

## Features

-   **SQLi Detection:** Classifies SQL queries to identify potential injection attacks.
-   **Dual Interface:** Use it as a simple **command-line tool** or as a **Python library**.
-   **Detailed Reporting:** Provides a detailed feature report for in-depth query analysis (CLI).
-   **Lightweight:** Minimal dependencies and a small footprint.

## Installation

Install SQShield from PyPI using pip:

```bash
pip install sqshield
```

Alternatively, for development, you can clone the repository and install it in editable mode:

```bash
git clone https://github.com/Pranav-2812/sqshield.git
cd sqshield
pip install -e .
```

## Usage

You can use SQShield as a command-line tool or as a Python library in your application.

### Command-Line Interface (CLI)

The primary command is `sqshield`, which accepts a SQL query string as an argument.

**Basic Prediction**

To check a query, pass it as an argument:

```bash
sqshield "SELECT * FROM users WHERE id = '1' OR '1'='1'"
```

**Expected Output:**
```
Query is MALICIOUS
```

To check a benign query:
```bash
sqshield "SELECT * FROM products WHERE category = 'electronics'"
```

**Expected Output:**
```
Query is BENIGN
```

**Get a Detailed Report**

For a more detailed analysis, use the `--report` or `-r` flag. This shows the feature vector used by the model for its prediction.

```bash
sqshield "SELECT * FROM users" --report
```

**Expected Output:**
```
   query_length  has_mixed_case  ...
0            19               0  ...
```
*(Note: The output will be a pandas DataFrame representation of the query's features.)*

**Check Version**

To display the installed version of SQShield, use the `--version` or `-v` flag:

```bash
sqshield --version
```

**Expected Output:**
```
sqshield version : 0.1.2
```

### Python API Usage

You can also integrate SQShield directly into your Python code. The primary function is `predict()`, which takes a query string and returns a prediction.

**Basic Prediction**

Import the `predict` function and pass a query string to it. The function returns `[1]` for a malicious query and `[0]` for a benign one.

```python
from sqshield import predict

# --- Example 1: Malicious Query ---
malicious_query = "SELECT * FROM users WHERE id = '1' OR '1'='1'"
prediction = predict(malicious_query)

print(f"Query: '{malicious_query}'")
if prediction[0] == 1:
    print("Result: Malicious")
else:
    print("Result: Benign")

# Expected Output:
# Query: 'SELECT * FROM users WHERE id = '1' OR '1'='1''
# Result: Malicious


# --- Example 2: Benign Query ---
benign_query = "SELECT * FROM products WHERE category = 'electronics'"
prediction = predict(benign_query)

print(f"Query: '{benign_query}'")
if prediction[0] == 1:
    print("Result: Malicious")
else:
    print("Result: Benign")

# Expected Output:
# Query: 'SELECT * FROM products WHERE category = 'electronics''
# Result: Benign
```

## API Reference (Quick)

While `predict` is the primary function, the following feature extraction functions are also available for advanced use:

-   `predict(query: str) -> list[bool]`: Predicts if a query is malicious. Returns `[1]` for malicious, `[0]` for benign.
-   `get_query_length(query: str) -> int`: Returns the length of the query.
-   `has_mixed_case(query: str) -> int`: Returns `1` if the query has mixed case, `0` otherwise.
-   `get_comment_count(query: str) -> int`: Counts comment indicators (`--`, `#`).
-   `get_special_char_count(query: str) -> int`: Counts various special characters.
-   `get_keyword_count(query: str) -> int`: Counts common SQL keywords.
-   `get_tautology_count(query: str) -> int`: Counts tautological patterns (e.g., `1=1`).
-   `get_time_based_keyword_count(query: str) -> int`: Counts time-based attack keywords (e.g., `sleep`).
-   `preprocess_query(query: str) -> pd.DataFrame`: Creates a feature DataFrame from a raw query for the model.

## How It Works

SQShield processes each input query by extracting a set of lexical features. These features, which include query length, keyword counts (e.g., `SELECT`, `UNION`), special character frequencies, and structural properties, are fed into a LightGBM classification model trained specifically on SQL query patterns. The model then predicts whether the query is `MALICIOUS` or `BENIGN`.

The model (`sql_injection_model.pkl`) is included with the package.

## Contributing

Contributions are welcome! If you have suggestions for improvements or find any bugs, please feel free to open an issue or submit a pull request.

1.  Fork the repository.
2.  Create a new feature branch (`git checkout -b feature/your-feature`).
3.  Commit your changes (`git commit -m 'Add some feature'`).
4.  Push to the branch (`git push origin feature/your-feature`).
5.  Open a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.