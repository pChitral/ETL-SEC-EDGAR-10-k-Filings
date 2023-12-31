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

11 directories, 23 files

The documentation of ETL-10-K-Filings is meticulously crafted to guide users through the project's intricacies. It covers the detailed architecture of the project, including setup instructions, a comprehensive workflow description, and guidelines for future developments and maintenance.

# Project Structure Overview of ETL-10-K-Filings

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

# Main Script Analysis of ETL-10-K-Filings

## Overview of `scrape_entire_text_mda.py`

The `scrape_entire_text_mda.py` script acts as the main entry point for the ETL-10-K-Filings project. It is responsible for initiating and coordinating the entire data extraction and processing pipeline.

### Role as the Entry Point

- **Central Coordinator**: This script kickstarts the ETL process, managing the flow and integration of various components.
- **Integration Point**: It seamlessly combines different modules and scripts, particularly from the `utils` directory, to perform the ETL tasks.

### Key Functionalities

- **Batch Processing of Tickers**: It efficiently handles the loading and processing of company tickers in batches, optimizing resource utilization.
- **Concurrent Processing**: Leverages `concurrent.futures` for multitasking, enhancing the speed and efficiency of data processing.
- **Logging and Status Tracking**: Employs robust logging for tracking the process flow and status, aiding in debugging and monitoring.

# Detailed Component Documentation of ETL-10-K-Filings

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

## Workflow Description

The ETL-10-K-Filings project follows a structured workflow, encompassing data download, processing, consolidation, and output generation. Each script and module in the `utils` directory plays a pivotal role in ensuring the smooth execution of each step in the workflow.

## Setting Up and Running the Project

Detailed instructions are provided for setting up the project environment, including the installation of dependencies and the execution of the main script, ensuring a smooth start-up for new users or developers.

## Logging and Error Handling

The project employs a comprehensive logging system to track progress and errors, facilitating debugging and ensuring transparency in the ETL process.

## Version Control and Collaboration

Version control practices and collaboration guidelines are outlined, promoting efficient and consistent contributions from multiple developers.

## Future Developments and Maintenance

Future plans for the project include potential expansions, improvements, and regular maintenance updates to adapt to evolving data structures and requirements.
