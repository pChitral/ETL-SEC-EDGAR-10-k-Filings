"""
This module contains a function to collect and organize ticker files from a specified data folder.
It uses the TickerFilesCollector class to gather files associated with various company tickers.
"""

import logging
from utils.file_operations.TickerFilesCollector import TickerFilesCollector


def collect_ticker_files(data_folder: str = "data/sec-edgar-filings") -> dict:
    """
    Collects and organizes ticker files from the specified data folder for all tickers.

    Parameters:
        data_folder (str, optional): The path to the root folder where company files are located.
                                     Default is 'data/sec-edgar-filings'.

    Returns:
        dict: A dictionary with company tickers as keys and lists of associated file paths as values.
    """
    try:
        # Create an instance of TickerFilesCollector
        ticker_collector = TickerFilesCollector(data_folder)

        # Get all ticker files from the collector
        return ticker_collector.get_all_ticker_files()

    except IOError as io_err:
        logging.error("I/O error occurred: %s", io_err)
        return {}
    except ValueError as val_err:
        logging.error("Value error occurred: %s", val_err)
        return {}
    # Add any other specific exceptions here.
    except Exception as e:
        # Catching a general exception as a fallback
        logging.error("An unexpected error occurred: %s", e)
        return {}
