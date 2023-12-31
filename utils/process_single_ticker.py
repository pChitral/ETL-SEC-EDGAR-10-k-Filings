from utils.process_ticker_10k_data import process_ticker_10k_data
import pandas as pd

from utils.delete_processed_folder import delete_processed_folder
import logging


def process_single_ticker(ticker, cik, title):
    """
    Process a single ticker's 10-K filings.
    """
    ticker_data = process_ticker_10k_data(ticker, cik, title)
    if ticker_data:
        ticker_df = pd.DataFrame(ticker_data)
        logging.info(f"Processed {len(ticker_df)} 10-K filings for {ticker}")
        # After successful processing and saving CSV, delete the folder
        delete_processed_folder(ticker)
        return ticker_df, cik, ticker
    else:
        logging.info(f"No data to process for ticker: {ticker}")
        return pd.DataFrame(), cik, ticker
