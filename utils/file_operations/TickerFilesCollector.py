import os
from typing import List, Dict, Any
from tqdm import tqdm


class TickerFilesCollector:
    def __init__(self, root_folder: str) -> None:
        """
        Initializes a TickerFilesCollector object.

        Parameters:
            root_folder (str): The path to the root folder where company files are located.
        """
        self.root_folder: str = root_folder
        self.ticker_files: Dict[str, List[str]] = {}
        self.total_tickers: int = 0  # Track the total number of tickers for tqdm

    def _collect_files(self, root_folder: str) -> List[str]:
        """
        Collects all TXT, HTML, and XML files inside the root_folder and its subfolders.

        Parameters:
            root_folder (str): The path to the folder to collect files from.

        Returns:
            List[str]: A list of file paths for TXT, HTML, and XML files found in the root_folder and its subfolders.
        """
        collected_files: List[str] = []
        for root, _, files in os.walk(root_folder):
            for file in files:
                if file.endswith((".txt", ".html", ".xml")):
                    collected_files.append(os.path.join(root, file))
        return collected_files

    def _get_ticker_files(self, root_folder: str, ticker: str) -> Dict[str, List[str]]:
        """
        Collects all TXT, HTML, and XML files for a specific ticker and stores them in a dictionary.

        Parameters:
            root_folder (str): The path to the folder to collect files from.
            ticker (str): The ticker symbol of the company associated with the files.

        Returns:
            Dict[str, List[str]]: A dictionary with 'ticker' as the key and a list of associated file paths as the value.
        """
        ticker_files: Dict[str, List[str]] = {ticker: self._collect_files(root_folder)}
        return ticker_files

    def get_all_ticker_files(self) -> Dict[str, List[str]]:
        """
        Collects all TXT, HTML, and XML files for all tickers in the root_folder.

        Returns:
            Dict[str, List[str]]: A dictionary with company tickers as keys and lists of associated file paths as values.
        """
        self.total_tickers = len(
            os.listdir(self.root_folder)
        )  # Get total number of tickers
        for folder in tqdm(
            os.listdir(self.root_folder), desc="Collecting Tickers", unit="ticker"
        ):
            ticker_folder = os.path.join(self.root_folder, folder)
            if os.path.isdir(ticker_folder):
                self.ticker_files.update(self._get_ticker_files(ticker_folder, folder))
        return self.ticker_files
