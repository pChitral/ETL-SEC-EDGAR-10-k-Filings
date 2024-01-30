# Introduction to ETL-10-K-Filings

## Overview

ETL-10-K-Filings is an advanced, Python-based project focused on the extraction, transformation, and loading (ETL) of financial data from SEC Edgar filings. Specifically targeting the Management's Discussion and Analysis (MDA) section from 10-K reports, the project processes a vast array of tickers, potentially exceeding 10,000, representing various publicly traded companies. The project, initially conceived to integrate with Supabase, has evolved to handle data through CSV files, enhancing scalability and data management efficiency.

## Project Goals

- **Automated Data Extraction**: Streamline the process of scraping the MDA section from 10-K filings for each unique company ticker.
- **Optimized Data Management**: Implement a system for temporary data storage, followed by deletion post-processing, to efficiently manage memory usage.
- **Concurrency in Processing**: Leverage multi-threading for faster and more efficient data processing.
- **Robust Data Recording**: Generate specific CSV files for each ticker, encompassing key details like CIK, ticker name, report year, and extracted text.

## Key Components

- **Data Folder**: Serves as a temporary holding area for downloaded files, which are cleared after processing.
- **Ticker Data Folder**: This folder is dedicated to storing the processed data for each ticker in CSV format, including crucial information and extracted text.
- **Utility Scripts**: The project features a suite of Python scripts and modules located in the `utils` directory, facilitating tasks such as data extraction, file operations, and data processing.
- **Logging Mechanism**: An integral logging system is implemented to monitor processing progress and provide informative updates on the project's status.

## Documentation Structure

```text
.
├── CODE_OF_CONDUCT.md
├── LICENSE
├── README.md
├── company_tickers.json
├── data
│   └── sec-edgar-filings
│       ├── AAPL
│       ├── GOOGL
│       └── MSFT
├── requirements.txt
├── scrape_entire_text_mda.py
└── utils
    ├── __init__.py
    ├── data_extraction
    │   ├── __init__.py
    │   └── extract_mda_section.py
    ├── file_operations
    │   ├── TickerFilesCollector.py
    │   ├── __init__.py
    │   ├── collect_ticker_files.py
    │   └── delete_txt_files.py
    ├── get_ticker_10k_filings.py
    ├── helpers
    │   ├── __init__.py
    │   ├── delete_processed_folder.py
    │   ├── initialize_status_file.py
    │   ├── update_status_file.py
    │   └── write_to_master_file.py
    └── processing
        ├── __init__.py
        ├── process_html_file.py
        ├── process_single_ticker.py
        └── process_ticker_10k_data.py

```

The documentation of ETL-10-K-Filings is meticulously crafted to guide users through the project's intricacies. It covers the detailed architecture of the project, including setup instructions, a comprehensive workflow description, and guidelines for future developments and maintenance.

## Project Structure Overview of ETL-10-K-Filings

## Folder Structure

The ETL-10-K-Filings project is organized into a structured directory system, facilitating ease of navigation and clarity in project management. Each directory and file plays a specific role in the project's operation:

- **`CODE_OF_CONDUCT.md`**: This file outlines the code of conduct for project contributors, fostering a respectful and collaborative development environment.
- **`LICENSE`**: Contains the licensing information, detailing the usage rights and restrictions associated with the project.
- **`README.md`**: Provides an introductory overview of the project, its purpose, and basic instructions for setup and usage.
- **`data` Directory**: Acts as temporary storage for downloaded files from SEC Edgar filings, which are processed and then deleted to maintain memory efficiency.
- **`ticker_data` Directory**: Stores processed data for each ticker in CSV format, containing vital information and extracted text.
- **`utils` Directory**: A collection of utility scripts and modules that perform various tasks, including data extraction, file operations, and processing. It is the backbone of the project.

## Significance of Each Component

Each component within the ETL-10-K-Filings is designed to serve a specific function, contributing to the overall efficiency and effectiveness of the project. The careful organization of files and directories ensures a systematic workflow, allowing for easy maintenance and scalability.

## Main Script Analysis of ETL-10-K-Filings

## Overview of `scrape_entire_text_mda.py`

The `scrape_entire_text_mda.py` script acts as the main entry point for the ETL-10-K-Filings project. It is responsible for initiating and coordinating the entire data extraction and processing pipeline.

### Role as the Entry Point

- **Central Coordinator**: This script kickstarts the ETL process, managing the flow and integration of various components.
- **Integration Point**: It seamlessly combines different modules and scripts, particularly from the `utils` directory, to perform the ETL tasks.

### Key Functionalities

- **Batch Processing of Tickers**: It efficiently handles the loading and processing of company tickers in batches, optimizing resource utilization.
- **Concurrent Processing**: Leverages `concurrent.futures` for multitasking, enhancing the speed and efficiency of data processing.
- **Logging and Status Tracking**: Employs robust logging for tracking the process flow and status, aiding in debugging and monitoring.

## Detailed Component Documentation of ETL-10-K-Filings

## Utils Module

### `helpers`:

- **Functions**:
  - `initialize_status_file`: Creates a status file to keep track of the processing stages of various tickers, ensuring organized progress monitoring.
  - `update_status_file`: Updates the status file post-processing of each ticker, reflecting the latest state of the workflow.
  - `write_to_master_file`: After processing all tickers, this function compiles the data into a comprehensive master file.

### `processing`:

- **Functionality**:
  - `process_single_ticker`: Dedicated to processing individual tickers, this script extracts and handles data for each specific ticker.
  - `process_html_file`: Specializes in extracting data from HTML files, transforming it into a structured and analyzable format.
  - `process_ticker_10k_data`: Manages the end-to-end processing of 10-K filings for each ticker, from initial extraction to final data output.

## File Operations

- **`TickerFilesCollector`**: This script is crucial in organizing the files related to each ticker, ensuring a structured approach to file handling.
- **`delete_txt_files`**: Focuses on clearing temporary text files after processing, playing a key role in managing memory and storage.
- **`collect_ticker_files`**: Gathers and sorts files for each ticker, preparing them for the processing stage.

## Data Extraction

- **`extract_mda_section`**:
  - **Purpose**: Targets the MDA section of 10-K filings for extraction, a critical component of financial analysis.
  - **Implementation**: Implements advanced text parsing techniques to accurately extract and isolate the MDA section.

Based on the provided code, here's a detailed documentation of the workflow for the ETL-10-K-Filings project:

## Workflow Description of ETL-10-K-Filings

The ETL-10-K-Filings project is designed to automate the extraction, transformation, and loading (ETL) of financial data from SEC Edgar filings, specifically targeting the Management's Discussion and Analysis (MDA) section of 10-K reports. The project's workflow is structured into several key stages, each facilitated by various scripts and modules:

### 1. Data Download and Preparation

- **Ticker File Collection**: The `TickerFilesCollector` class in `utils.file_operations` is responsible for collecting and organizing files related to each ticker symbol. It traverses through the `data/sec-edgar-filings` directory, gathering all relevant HTML, TXT, or XML files for each company ticker.
- **10-K Filing Download**: The function `get_ticker_10k_filings` utilizes the `sec_edgar_downloader` package to download 10-K filings from the SEC Edgar database. This function is equipped with rate limiting and retry logic to handle request limitations and ensure successful downloads.

### 2. Data Processing

- **Processing Single Ticker**: The `process_single_ticker` function from `utils.processing` is tasked with processing data for individual tickers. This involves extracting the MDA section from 10-K filings and other required data manipulations.
- **HTML File Processing**: For HTML files, `extract_mda_section` parses and extracts the MDA section, utilizing BeautifulSoup for HTML content parsing and regular expressions to locate specific sections within the document.

### 3. Data Consolidation and Output Generation

- **Master Data File Creation**: The `write_to_master_file` function handles the consolidation of all processed data into a master CSV file, `all_ticker_10k_mda_data.csv`. This function ensures thread-safe write operations to the CSV file using `FileLock`.
- **Status Tracking and Logging**: Throughout the process, the status of ticker processing is tracked and updated in `processing_status.csv` using `initialize_status_file` and `update_status_file` functions. Additionally, detailed logs of the process are maintained using Python’s logging module, aiding in monitoring and debugging.

### 4. Post-Processing Cleanup

- **Deleting Temporary Files and Folders**: After processing, temporary files (like text files) are deleted using the `delete_txt_files` function to free up memory space. Similarly, the `delete_processed_folder` function removes processed folders (e.g., 10-K filings folders) for each ticker to maintain efficiency in storage utilization.

### 5. Error Handling and Rate Limiting

- **Error Logging**: Errors encountered during the workflow are logged to `error_log.txt`, enabling easy identification and resolution of issues.
- **Rate Limiting**: The `pyrate_limiter` library is employed to manage request rates to the SEC Edgar database, minimizing the risk of exceeding API limits and ensuring smooth data retrieval.

### 6. Concurrent Processing

- **Batch Processing**: The project employs `concurrent.futures` for concurrent processing of tickers in batches, enhancing efficiency and reducing processing time. Each batch of tickers is processed in parallel, speeding up the overall workflow.

### 7. Miscellaneous Utilities

- **Miscellaneous Utilities**: The project also contains various other utility functions and classes that support the overall workflow, including handling file operations, data extraction, and processing tasks.

## Setting Up and Running the Project

The ETL-10-K-Filings project is designed to be user-friendly, allowing new users and developers to set up and run the project with ease. Here is a step-by-step guide to setting up the project environment and executing the main script:

### Step 1: Creating a Virtual Environment

- **Why Use a Virtual Environment?**: A virtual environment in Python is a self-contained directory that holds a Python installation for a particular version of Python, along with a number of additional packages. Using a virtual environment ensures that the dependencies required for this project do not interfere with other Python projects or system-wide packages.
- **How to Create a Virtual Environment**:
  1. Navigate to the project directory in the terminal or command prompt.
  2. Run `python3 -m venv venv` (This command creates a virtual environment named `venv` in the project directory. You can replace `venv` with any name you prefer for your virtual environment.)
  3. Activate the virtual environment:
     - On Windows, run `venv\Scripts\activate`.
     - On macOS and Linux, run `source venv/bin/activate`.

### Step 2: Installing Dependencies

- **Requirements File**: The project includes a `requirements.txt` file, which lists all the Python packages needed for the project to run.
- **Installing Dependencies**: With the virtual environment activated, install the required packages by running `pip install -r requirements.txt` in your terminal. This command will download and install all the dependencies listed in the `requirements.txt` file.

### Step 3: Running the Main Script

- **Main Script**: The main script for the project is `scrape_entire_text_mda.py`. This script is responsible for coordinating the entire data extraction and processing workflow.
- **Execution**: To run the main script, ensure you are still in the project's root directory with the virtual environment activated. Then execute the script by running `python scrape_entire_text_mda.py`.

### Step 4: Post-Execution Tasks

- **Review Output**: After running the script, check the output files and logs to ensure that the script has executed correctly and as expected.
- **Deactivating the Virtual Environment**: Once you are done working with the project, you can deactivate the virtual environment by simply running `deactivate` in your terminal.

## Logging and Error Handling

The ETL-10-K-Filings project incorporates a robust logging and error handling system, essential for tracking the progress of data processing, identifying issues, and ensuring a transparent ETL process.

### Logging System

- **Configuration**: The project is configured to use Python's built-in `logging` module, which allows for tracking events that occur while the software runs. The logging setup is defined in the main script and other relevant modules.
- **Log Levels**: Different log levels (INFO, WARNING, ERROR) are used to categorize the importance of the log messages. This helps in distinguishing between general information, potential issues to be aware of, and critical errors.
- **Log Output**: Log messages are directed to two main outputs:
  1. A log file (`ticker_processing.log`) which records all the events for later review. This file is particularly useful for post-run analysis and debugging.
  2. The console (or standard output stream), allowing real-time monitoring of the process.
- **Log Content**: The log messages include timestamps, log levels, and descriptive messages, providing clarity on what the system is doing at any given time and making it easier to trace and understand the flow of execution.

### Error Handling

- **Exception Logging**: In cases of exceptions or errors, the script logs detailed error messages. This includes the type of error, a descriptive message, and, in many cases, the stack trace.
- **Error Recovery**: For non-critical errors, the system is designed to log the error and continue processing. This approach ensures that temporary issues or errors with specific data points don't halt the entire ETL process.

### Managing External Logs

- **Reducing Log Clutter from `pyrate_limiter`**: The project uses the `pyrate_limiter` library for rate limiting API calls. By default, `pyrate_limiter` logs many informational messages, which can clutter the log file and obscure more important messages.
- **Filtering Out Unnecessary Logs**: To improve log interpretability and manage the size of the log file, informational logs from `pyrate_limiter` are suppressed. This is achieved by setting the logging level of `pyrate_limiter` to WARNING or higher, ensuring that only significant events from this library are recorded.

### Benefits of the Logging and Error Handling System

- **Debugging**: The detailed logs provide essential insights for debugging. By analyzing the log files, developers can pinpoint where and why an error occurred.
- **Transparency**: Logging keeps a record of the project's operations, offering transparency in how data is processed and handled.
- **Maintainability**: A well-maintained log aids in the ongoing maintenance and enhancement of the project, as it provides historical data on the system’s behavior and issues.

## Version Control and Collaboration

The ETL-10-K-Filings project emphasizes the importance of effective version control and collaboration practices to ensure smooth and productive contributions from multiple developers. Here's an overview of the guidelines and systems in place:

### Collaboration Guidelines

- **Code Reviews**: Each PR should be reviewed by at least one other team member. Code reviews ensure that the new code aligns with the project's standards and goals.
- **Issue Tracking**: GitHub Issues is used for tracking tasks, bugs, and feature requests. It’s a great tool for organizing work and discussions around specific topics or problems.
- **Documentation Updates**: Alongside code changes, updating relevant documentation is crucial. This ensures that the documentation stays current and helpful for all contributors.
- **Branching Strategy**: Developers are encouraged to use feature branching, where new features or bug fixes are developed in separate branches and then merged into the main branch upon completion. This strategy helps in isolating changes and ensuring stability in the main codebase.

### Commit Messages and Code Standards

- **Clear Commit Messages**: Contributors are encouraged to write clear, concise commit messages that describe the changes made and their purpose. This practice improves the readability and traceability of the project history.
- **Coding Standards**: Adherence to a consistent coding style is vital for maintainability and readability. The project may define specific coding standards or follow widely accepted conventions for Python.
- **Pull Requests (PRs)**: Changes to the codebase should be submitted through PRs. This process allows for code review and discussion before changes are integrated.

### Encouraging Open Communication

- **Discussion and Feedback**: Open communication is encouraged among team members. Developers should feel free to discuss ideas, provide feedback, and ask for help when needed.
- **Respectful and Constructive Interactions**: All interactions within the project should be respectful and constructive, fostering a positive and collaborative environment.

## Future Developments and Maintenance

Future plans for the project include potential expansions, improvements, and regular maintenance updates to adapt to evolving data structures and requirements.
