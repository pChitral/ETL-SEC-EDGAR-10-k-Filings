# ETL for SEC Edgar 10-K Filings Processor

## Table of Contents
1. [Overview](#overview)
2. [Folder Structure](#folder-structure)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Data Processing Pipeline](#data-processing-pipeline)
6. [Supabase Integration](#supabase-integration)
7. [Memory Efficiency](#memory-efficiency)
8. [Contributing](#contributing)
9. [License](#license)
10. [Acknowledgments](#acknowledgments)

## Overview
The `ETL-10-k-Filings` project is designed to process and manage 10-K filings data for numerous companies from the SEC Edgar website. Through a set of utility functions housed within the `utils` folder, the project efficiently processes the data of over 10,000 tickers, facilitating in-depth analysis and research.

## Folder Structure
```plaintext
ETL-10-k-Filings/
|-- CODE_OF_CONDUCT.md
|-- LICENSE
|-- README.md
|-- company_tickers.json
|-- data
|-- mdna_output.txt
|-- parsing.ipynb
|-- requirements.txt
|-- script.py
|-- utils/
    |-- (various utility scripts)
|-- venv
|-- wc_scripy.py
|-- word_count.ipynb
|-- words_fraud_constraints.json
```

## Installation
1. Clone the repository.
2. Navigate to the project directory.
3. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
4. Activate the virtual environment:
   ```bash
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
5. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Ensure the virtual environment is activated.
2. Run the main script to process the 10-K filings data:
   ```bash
   python script.py
   ```

## Data Processing Pipeline
The main script (`script.py`) initiates the data processing pipeline by reading company tickers from `company_tickers.json`. It iterates through each ticker and invokes the `process_ticker_10k_data` function from `utils.process_ticker_10k_data` to process the 10-K filings data for each ticker. The processed data is collected in a dictionary for further analysis or utilization.

The `process_ticker_10k_data` function performs several steps:
- Downloads the 10-K filings for a given ticker using `get_ticker_10k_filings`.
- Collects and organizes the downloaded files with `collect_ticker_files`.
- Deletes unnecessary text files to save space.
- Parses the HTML files to extract relevant data.
- Constructs a dictionary with the parsed data.
- Pushes the parsed data to Supabase using `new_10k_reports_to_supabase_mda`.

## Supabase Integration
The project integrates with Supabase for data storage and management. The `new_10k_reports_to_supabase_mda` function in `utils` pushes the processed data to Supabase, leveraging the Supabase client configured with the provided API keys.

## Memory Efficiency
The project is engineered for memory efficiency, capable of processing 2.5 TB worth of data while only requiring an average of 250 MB memory at runtime. This efficiency is achieved by processing the 10-K filings of a specific ticker one at a time, minimizing the memory footprint.

## Contributing
If you wish to contribute to this project, we welcome your contributions! Please follow the guidelines in `CODE_OF_CONDUCT.md` for information on how to get started.

## License
This project is licensed under the MIT License. You are free to use, modify, and distribute the code.

## Acknowledgments
Special thanks to all contributors who have invested their time and effort into this project. Your contributions are highly valued.

