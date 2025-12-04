
# SQShield: SQL Injection Detection Tool

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![PyPI Version](https://img.shields.io/pypi/v/sqshield.svg)

SQShield is a command-line tool designed to detect potential SQL injection (SQLi) attacks in your queries. It leverages a pre-trained machine learning model to classify queries as either malicious or benign, helping you secure your applications against common database threats.

## Features

-   **SQLi Detection:** Classifies SQL queries to identify potential injection attacks.
-   **Easy to Use:** Simple and intuitive command-line interface.
-   **Detailed Reporting:** Provides a detailed feature report for in-depth query analysis.
-   **Lightweight:** Minimal dependencies and a small footprint.

## Installation

You can install SQShield directly from this repository.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/sqshield.git
    cd sqshield
    ```

2.  **Install the package:**
    For development or local installation, use `pip` with the editable flag:
    ```bash
    pip install -e .
    ```
    This will install the package and make the `sqshield` command available in your shell.

## Usage

The primary command is `sqshield`, which accepts a SQL query string as an argument.

### Basic Prediction

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
Query is BENGIN
```

### Get a Detailed Report

For a more detailed analysis, use the `--report` or `-r` flag. This shows the feature vector used by the model for its prediction.

```bash
sqshield "SELECT * FROM users" --report
```

**Expected Output:**
```
 query_length  ...  semicolon_count
          19   ...                0
```
*(Note: The output will be a full DataFrame representation of the query's features.)*

### Check Version

To display the installed version of SQShield, use the `--version` or `-v` flag:

```bash
sqshield --version
```

**Expected Output:**
```
sqshield version : 0.1.0
```

## How It Works

SQShield processes each input query by extracting a set of lexical features. These features, which include query length, keyword counts (e.g., `SELECT`, `UNION`), special character frequencies, and structural properties, are fed into a pre-trained LightGBM classification model. The model then predicts whether the query is `MALICIOUS` or `BENGIN`.

The model (`sql_injection_model.pkl`) is included with the package.

## Contributing

Contributions are welcome! If you have suggestions for improvements or find any bugs, please feel free to open an issue or submit a pull request.

1.  Fork the repository.
2.  Create a new feature branch (`git checkout -b feature/your-feature`).
3.  Commit your changes (`git commit -m 'Add some feature'`).
4.  Push to the branch (`git push origin feature/your-feature`).
5.  Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
