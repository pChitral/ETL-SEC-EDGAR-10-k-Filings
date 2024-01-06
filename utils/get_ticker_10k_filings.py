import logging
import time
from typing import Union

from sec_edgar_downloader import Downloader
from requests.exceptions import HTTPError

# Set the logging level for pyrate_limiter to WARNING or higher to suppress INFO messages
logging.getLogger("pyrate_limiter").setLevel(logging.WARNING)


def get_ticker_10k_filings(
    cik: Union[str, int],
    max_retries: int = 5,
    initial_backoff: float = 2.0,
    backoff_factor: float = 2.0,
) -> bool:
    """
    Enhanced downloading of 10-K filings with refined rate limiting and retry logic.

    Args:
        cik (Union[str, int]): Central Index Key (CIK) of the company.
        max_retries (int): Maximum number of retry attempts.
        initial_backoff (float): Initial time to wait between retry attempts.
        backoff_factor (float): Factor by which to increase backoff time after each attempt.

    Returns:
        bool: True if download succeeds, False otherwise.
    """
    dl = Downloader("SUNY_Buffalo", "hello@buffalo.edu", "data")
    sleep_time = initial_backoff

    for attempt in range(max_retries):
        try:
            dl.get("10-K", cik, download_details=True)
            return True
        except HTTPError as e:
            if e.response.status_code == 429:
                logging.warning(
                    "Rate limit exceeded for CIK %s. Retrying in %s seconds.",
                    cik,
                    sleep_time,
                )
            else:
                logging.error("HTTP error for CIK %s: %s", cik, e)
        except Exception as e:
            logging.error("Attempt %s failed for CIK %s: %s", attempt + 1, cik, e)

        if attempt < max_retries - 1:
            time.sleep(sleep_time)
            sleep_time = min(
                sleep_time * backoff_factor, 120
            )  # Cap the sleep time at 120 seconds

    logging.error(f"All attempts to download 10-K filings for CIK {cik} have failed.")
    return False
