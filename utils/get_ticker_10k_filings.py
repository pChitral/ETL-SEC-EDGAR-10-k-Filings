import logging
import time
from sec_edgar_downloader import Downloader
from requests.exceptions import HTTPError
import random

# Set the logging level for pyrate_limiter to WARNING or higher to suppress INFO messages
logging.getLogger("pyrate_limiter").setLevel(logging.WARNING)


def get_ticker_10k_filings(ticker):
    """
    Download 10-K filings for a single ticker.
    """
    dl = Downloader("SUNY_Buffalo", "hello@buffalo.edu", "data")

    try:
        # Introduce a random sleep time to avoid hitting rate limits
        time.sleep(random.uniform(1, 2))

        # Download 10-K filings for the given ticker
        dl.get("10-K", ticker, download_details=True)

        # Log successful download
        logging.info(f"Successfully downloaded 10-K filings for ticker {ticker}.")
        return True
    except HTTPError as e:
        logging.error(f"HTTP error for ticker {ticker}: {e}")
    except Exception as e:
        logging.error(f"Error occurred while downloading filings for ticker {ticker}: {e}")

    return False
