import shutil
import logging


def delete_processed_folder(ticker):
    """
    Deletes the 10-K filings folder for the specified ticker.

    Args:
    - ticker (str): Ticker symbol of the company.
    """
    folder_path = f"data/sec-edgar-filings/{ticker}/10-K"
    try:
        shutil.rmtree(folder_path)
        logging.info(f"Successfully deleted 10-K filings folder for {ticker}")
    except Exception as e:
        logging.error(f"Error deleting 10-K filings folder for {ticker}: {e}")
