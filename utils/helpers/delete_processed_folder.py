import shutil
import logging
from typing import NoReturn


def delete_processed_folder(ticker: str) -> NoReturn:
    """
    Deletes the 10-K filings folder for the specified ticker.

    Args:
        ticker (str): Ticker symbol of the company.

    Returns:
        NoReturn: This function does not return anything. It performs a deletion operation.
    """
    folder_path = f"data/sec-edgar-filings/{ticker}/10-K"
    try:
        shutil.rmtree(folder_path)
        logging.info(f"Successfully deleted 10-K filings folder for {ticker}")
    except FileNotFoundError:
        logging.error(f"10-K filings folder for {ticker} not found.")
    except OSError as e:
        logging.error(f"Error deleting 10-K filings folder for {ticker}: {e}")
