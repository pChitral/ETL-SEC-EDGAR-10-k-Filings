# ETL for SEC Edgar 10-K Filings Downloader"

## Table of Contents

- [Project Documentation: 10k-download](#project-documentation-10k-download)
  - [Table of Contents](#table-of-contents)
  - [1. Overview ](#1-overview-)
  - [2. Folder Structure ](#2-folder-structure-)
  - [3. Module: TickerFilesCollector ](#3-module-tickerfilescollector-)
    - [3.1. Methods ](#31-methods-)
  - [4. Module: collect\_ticker\_files ](#4-module-collect_ticker_files-)
    - [4.1. Function ](#41-function-)
  - [5. Module: get\_ticker\_10k\_filings ](#5-module-get_ticker_10k_filings-)
    - [5.1. Function ](#51-function-)
  - [6. Usage Examples ](#6-usage-examples-)
  - [7. License ](#7-license-)
  - [8. Contributing ](#8-contributing-)
  - [9. Acknowledgments ](#9-acknowledgments-)

---

## 1. Overview <a name="1-overview"></a>

The 10k-download project provides utilities for downloading, collecting, and organizing 10-K filings for various companies from the SEC Edgar website. This open-source project consists of modules that facilitate file collection, 10-K download, and usage examples for a seamless experience.

---

## 2. Folder Structure <a name="2-folder-structure"></a>

```plaintext
10k-download/
|-- CODE_OF_CONDUCT.md
|-- README.md
|-- myenv/
|-- requirements.txt
|-- LICENSE
|-- data/
|-- playground.ipynb
|-- utils/
    |-- TickerFilesCollector.py
    |-- __init__.py
    |-- __pycache__/
    |-- collect_ticker_files.py
    |-- get_ticker_10k_filings.py

```

- **`myenv/`**: Virtual environment directory for managing project dependencies.
- **`playground.ipynb`**: A Jupyter notebook for testing and usage examples.
- **`requirements.txt`**: A text file containing required Python packages.
- **`utils/`**: A directory containing utility modules.
  - **`TickerFilesCollector.py`**: Module for collecting ticker files.
  - **`__init__.py`**: Initialization file for the `utils` package.

---

## 3. Module: TickerFilesCollector <a name="3-module-tickerfilescollector"></a>

The `TickerFilesCollector` class in the `TickerFilesCollector.py` module is responsible for collecting and organizing ticker files from the specified data folder.

### 3.1. Methods <a name="31-methods"></a>

- `__init__(self, root_folder)`: Initializes a `TickerFilesCollector` object.
- `_collect_files(self, root_folder)`: Collects all TXT, HTML, and XML files inside the `root_folder` and its subfolders.
- `_get_ticker_files(self, root_folder, ticker)`: Collects all TXT, HTML, and XML files for a specific ticker and stores them in a dictionary.
- `get_all_ticker_files(self)`: Collects all TXT, HTML, and XML files for all tickers in the `root_folder`.

---

## 4. Module: collect_ticker_files <a name="4-module-collect_ticker_files"></a>

The `collect_ticker_files.py` module provides the `collect_ticker_files` function, which is responsible for collecting and organizing ticker files from the specified data folder for all tickers.

### 4.1. Function <a name="41-function"></a>

- `collect_ticker_files(data_folder='data/sec-edgar-filings')`: Collects and organizes ticker files from the specified data folder for all tickers.

---

## 5. Module: get_ticker_10k_filings <a name="5-module-get_ticker_10k_filings"></a>

The `get_ticker_10k_filings.py` module provides the `get_ticker_10k_filings` function, which downloads all the 10-K filings for a given ticker from the SEC Edgar website.

### 5.1. Function <a name="51-function"></a>

- `get_ticker_10k_filings(ticker)`: Downloads all the 10-K filings for a given `ticker` from the SEC Edgar website.

---

## 6. Usage Examples <a name="6-usage-examples"></a>

For detailed usage examples and demonstrations of the project functionalities, refer to the `playground.ipynb` Jupyter notebook in the root directory.

---

## 7. License <a name="7-license"></a>

This project is licensed under the [MIT License](LICENSE). You are free to use, modify, and distribute the code.

---

## 8. Contributing <a name="8-contributing"></a>

If you wish to contribute to this project, we welcome your contributions! Please follow the guidelines in [CONTRIBUTING.md](CONTRIBUTING.md) for information on how to get started.

---

## 9. Acknowledgments <a name="9-acknowledgments"></a>

Special thanks to all the contributors who have contributed to this project. Your efforts are greatly appreciated

That should be a more professional and organized documentation for your 10k-download project. It includes a clear table of contents, detailed explanations for each section, and proper formatting to make it look like a typical open-source project's README on GitHub. The license, contributing guidelines, and acknowledgments sections provide the necessary information for potential users and contributors.

Remember to update the actual content of the sections with the relevant information for your project. This includes adding descriptions of the project's functionalities, installation instructions, and usage examples in the "Usage Examples" section. Additionally, make sure to include details about how users can set up their development environment and run the project.

If you have any more specific questions or need further assistance, feel free to ask!
