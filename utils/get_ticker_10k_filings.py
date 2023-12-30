import logging
import time
from sec_edgar_downloader import Downloader


def get_ticker_10k_filings(ticker, max_retries=5, backoff_factor=1.0):
    """
    Downloads all the 10-K filings for a given ticker from the SEC Edgar website with retry logic.

    Parameters:
        ticker (str): The ticker symbol of the company whose 10-K filings are to be downloaded.
        max_retries (int): Maximum number of retry attempts.
        backoff_factor (float): Factor to determine the wait time between retries.

    Returns:
        bool: True if the download is successful, False otherwise.

    Example:
        get_ticker_10k_filings("MSFT")
    """

    # Create a downloader instance with the "data" folder as the destination
    dl = Downloader("SUNY_Buffalo", "hello@buffalo.edu", "data")

    for attempt in range(max_retries):
        try:
            # Get all 10-K filings for the specified ticker
            dl.get("10-K", ticker, download_details=True)
            return True  # Successful download
        except Exception as e:
            logging.error(f"Attempt {attempt + 1} failed for {ticker}: {e}")

            # Calculate sleep time using exponential backoff strategy
            sleep_time = backoff_factor * (2**attempt)
            time.sleep(sleep_time)

    # If all attempts fail, log and return False
    logging.error(f"All attempts to download 10-K filings for {ticker} have failed.")
    return False


# Example usage:
if __name__ == "__main__":
    # Set up logging configuration to save errors to a file
    logging.basicConfig(
        filename="error_log.txt",
        level=logging.ERROR,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    ticker_name = "MSFT"  # Replace this with the desired ticker name
    success = get_ticker_10k_filings(ticker_name)

    if not success:
        logging.error(f"Failed to download filings for {ticker_name}")
