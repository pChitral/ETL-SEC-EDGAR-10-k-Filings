"""
This module provides functions related to initializing and managing a status file for processing data.
It includes functionality to create a new status file with unprocessed tickers if such a file doesn't already exist.
"""

import os
import pandas as pd
from typing import NoReturn


def initialize_status_file(df: pd.DataFrame) -> NoReturn:
    """
    Initializes a status file to track the processing status of tickers. If the status file does not exist,
    it creates a new one with all tickers marked as unprocessed.

    Args:
        df (pd.DataFrame): A DataFrame containing tickers to be initialized in the status file.

    Returns:
        NoReturn: This function does not return anything. It creates or updates a file.
    """
    status_file = "processing_status.csv"
    if not os.path.exists(status_file):
        status_df = pd.DataFrame({"ticker": df["ticker"], "processed": False})
        status_df.to_csv(status_file, index=False)
