import logging
import time
from sec_edgar_downloader import Downloader
from requests.exceptions import HTTPError
import random

# Set the logging level for pyrate_limiter to WARNING or higher to suppress INFO messages
logging.getLogger("pyrate_limiter").setLevel(logging.WARNING)


def get_ticker_10k_filings(cik):
    """
    Download 10-K filings for a single CIK.
    """
    dl = Downloader("SUNY_Buffalo", "hello@buffalo.edu", "data")

    try:
        # Introduce a random sleep time to avoid hitting rate limits
        time.sleep(random.uniform(1, 2))

        # Download 10-K filings for the given CIK
        dl.get("10-K", cik, download_details=True)

        # Log successful download
        logging.info(f"Successfully downloaded 10-K filings for CIK {cik}.")
        return True
    except HTTPError as e:
        logging.error(f"HTTP error for CIK {cik}: {e}")
    except Exception as e:
        logging.error(f"Error occurred while downloading filings for CIK {cik}: {e}")

    return False
