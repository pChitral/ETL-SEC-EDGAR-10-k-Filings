import logging
from utils.TickerFilesCollector import TickerFilesCollector


def collect_ticker_files(data_folder="data/sec-edgar-filings"):
    """
    Collects and organizes ticker files from the specified data folder for all tickers.

    Parameters:
        data_folder (str, optional): The path to the root folder where company files are located. Default is 'data/sec-edgar-filings'.

    Returns:
        dict: A dictionary with company tickers as keys and lists of associated file paths as values.
    """
    try:
        # Create an instance of TickerFilesCollector
        ticker_collector = TickerFilesCollector(data_folder)

        # Get all ticker files from the collector
        all_ticker_files = ticker_collector.get_all_ticker_files()

        # Print and return the collected files dictionary
        for ticker, ticker_files in all_ticker_files.items():
            print(f"Files are ready for {ticker}")

        return all_ticker_files

    except Exception as e:
        # Log the error message
        logging.error(f"Error occurred while collecting ticker files: {e}")
        return None


if __name__ == "__main__":
    # Set up logging configuration to save errors to a file
    logging.basicConfig(
        filename="error_log.txt",
        level=logging.ERROR,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    all_ticker_files = collect_ticker_files()  # Uses the default data folder
