# Standard library imports
import concurrent.futures
import logging

# Local application imports from utils module
from utils.get_ticker_10k_filings import get_ticker_10k_filings
from utils.file_operations.collect_ticker_files import collect_ticker_files
from utils.file_operations.delete_txt_files import delete_txt_files
from utils.processing.process_html_file import process_html_file


def process_ticker_10k_data(ticker, cik, title):
    """
    Process the 10-K filings for a given ticker.

    This function manages the entire process of downloading, collecting, and processing
    the HTML files of 10-K filings associated with a specific ticker.

    Args:
    - ticker (str): Ticker symbol of the company.
    - cik (str): Central Index Key (CIK) of the company.
    - title (str): The title associated with the company or filing.

    Returns:
    - list: A list of dictionaries, each containing the parsed data for a single 10-K filing.
    """

    
    # Collect the downloaded ticker files
    ticker_files_dict = collect_ticker_files()

    # Delete any text files associated with the ticker, if any
    delete_txt_files(ticker_files_dict.get(ticker, []))

    # Retrieve the list of HTML files for the ticker
    html_files = ticker_files_dict.get(ticker, [])

    # Process each HTML file in parallel using ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Map each file to the processing function and collect results
        results = executor.map(
            lambda file: process_html_file(file, ticker, cik, title), html_files
        )

        # Compile all parsed data into a list, filtering out None results
        all_parsed_data = {
            result["processed_timestamp"]: result
            for result in results
            if result is not None
        }

    # Convert the dictionary of parsed data to a list
    all_parsed_data_list = list(all_parsed_data.values())
    logging.info(
        f"Completed processing {len(all_parsed_data_list)} HTML files for {ticker}"
    )

    return all_parsed_data_list
