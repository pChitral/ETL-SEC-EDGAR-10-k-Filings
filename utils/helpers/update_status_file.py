"""
This module contains functions to update the processing status of tickers in a CSV file. 
It provides functionalities to mark a specific ticker as processed.
"""

import pandas as pd
from typing import NoReturn


def update_status_file(ticker: str) -> NoReturn:
    """
    Updates the processing status of a given ticker in a CSV file to True.

    Args:
        ticker (str): The ticker symbol of the company whose processing status needs to be updated.

    Returns:
        NoReturn: This function does not return anything. It updates a CSV file.
    """
    status_file = "processing_status.csv"
    status_df = pd.read_csv(status_file)
    status_df.loc[status_df["ticker"] == ticker, "processed"] = True
    status_df.to_csv(status_file, index=False)
