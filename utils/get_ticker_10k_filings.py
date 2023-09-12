import logging
from sec_edgar_downloader import Downloader


def get_ticker_10k_filings(ticker):
    """
    Downloads all the 10-K filings for a given ticker from the SEC Edgar website.

    Parameters:
        ticker (str): The ticker symbol of the company whose 10-K filings are to be downloaded.

    Returns:
        None

    Raises:
        Exception: If any error occurs during the file download process, it will be logged.

    Example:
        get_ticker_10k_filings("MSFT")
    """
    # Create a downloader instance with the "data" folder as the destination
    dl = Downloader("SUNY_Buffalo", "hello@buffalo.edu", "data")

    try:
        # Get all 10-K filings for the specified ticker
        # Use tqdm to add the progress bar
        dl.get("10-K", ticker, download_details=True)
    except Exception as e:
        # Log the error message along with the ticker symbol
        logging.error(
            f"Error occurred while downloading 10-K filings for {ticker}: {e}"
        )


# Example usage:
if __name__ == "__main__":
    # Set up logging configuration to save errors to a file
    logging.basicConfig(
        filename="error_log.txt",
        level=logging.ERROR,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    ticker_name = "MSFT"  # Replace this with the desired ticker name
    get_ticker_10k_filings(ticker_name)
