"""
This module contains functions for handling and processing data related to company tickers, 
specifically writing data to a master CSV file with thread safety.
"""

from filelock import FileLock
import pandas as pd
from typing import NoReturn


def write_to_master_file(master_df: pd.DataFrame) -> NoReturn:
    """
    Writes the contents of a pandas DataFrame to a CSV file, ensuring thread-safe file access
    using a file lock.

    Args:
        master_df (pd.DataFrame): The pandas DataFrame to be written to the CSV file.

    Returns:
        NoReturn: This function does not return anything. It performs a file write operation.
    """
    with FileLock("all_ticker_10k_mda_data.csv.lock"):
        master_df.to_csv("all_ticker_10k_mda_data.csv", index=False)
