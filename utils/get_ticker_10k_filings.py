import logging
import time
from sec_edgar_downloader import Downloader
from requests.exceptions import HTTPError
import random


# Set the logging level for pyrate_limiter to WARNING or higher to suppress INFO messages
logging.getLogger("pyrate_limiter").setLevel(logging.WARNING)


def get_ticker_10k_filings(cik, max_retries=2, initial_backoff=2.0, backoff_factor=2.0):
    """
    Enhanced downloading of 10-K filings with refined rate limiting and retry logic.
    """
    dl = Downloader("SUNY_Buffalo", "hello@buffalo.edu", "data")
    sleep_time = initial_backoff

    for attempt in range(max_retries):
        try:
            time.sleep(random.uniform(1, 2))
            dl.get("10-K", cik, download_details=True)
            # Reset sleep time after successful request and return True
            return True
        except HTTPError as e:
            if e.response.status_code == 429:
                logging.warning(
                    f"Rate limit exceeded for CIK {cik}. Retrying in {sleep_time} seconds."
                )
            else:
                logging.error(f"HTTP error for CIK {cik}: {e}")
        except Exception as e:
            logging.error(f"Attempt {attempt + 1} failed for CIK {cik}: {e}")

        if attempt < max_retries - 1:
            time.sleep(sleep_time)
            sleep_time = min(
                sleep_time * backoff_factor, 120
            )  # Cap the sleep time at 120 seconds

    logging.error(f"All attempts to download 10-K filings for CIK {cik} have failed.")
    return False
