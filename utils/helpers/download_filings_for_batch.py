"""
This module provides functionalities to download financial filings for a list of tickers
using concurrent requests while respecting a rate limit.
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
import random
import threading
import time
from requests.exceptions import HTTPError, RequestException

from utils.get_ticker_10k_filings import get_ticker_10k_filings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Semaphore to limit the number of requests to 10 per second
REQUEST_SEMAPHORE = threading.Semaphore(10)


def download_filings(ticker, retry_delay=0):
    """
    Downloads filings for a given ticker with an optional delay.

    Args:
        ticker (str): The ticker symbol for which to download filings.
        retry_delay (float): The delay in seconds before making a request.

    Returns:
        bool: True if download succeeded, False otherwise.
    """
    time.sleep(retry_delay)  # Delay before making the request

    with REQUEST_SEMAPHORE:
        try:
            time.sleep(random.uniform(1, 2))
            success = get_ticker_10k_filings(ticker)
            return success
        except HTTPError as e:
            if e.response.status_code == 429:
                logging.error(f"Rate limit exceeded for {ticker}")
            else:
                logging.error(f"HTTP error occurred for {ticker}: {e}")
        except RequestException as e:
            logging.error(f"Request exception for {ticker}: {e}")
        except Exception as e:
            logging.error(f"General error occurred for {ticker}: {e}")

        return False


def download_filings_for_batch(ticker_list, max_retries=3):
    """
    Downloads filings for a batch of tickers with retry logic.

    Args:
        ticker_list (list of str): List of ticker symbols to process.
        max_retries (int): Maximum number of retries for each ticker.

    Returns:
        None
    """
    retry_counts = {ticker: 0 for ticker in ticker_list}
    to_retry = set(ticker_list)

    while to_retry:
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_ticker = {
                executor.submit(
                    download_filings,
                    ticker,
                    2 ** retry_counts[ticker] + random.uniform(0, 1),
                ): ticker
                for ticker in to_retry
            }
            to_retry.clear()

            for future in as_completed(future_to_ticker):
                ticker = future_to_ticker[future]
                success = future.result()
                if success:
                    print(f"Successfully from download_filings_for_batch for ticker: {ticker}") 
                    # logging.info(
                    #     f"Successfully downloaded filings for ticker: {ticker}"
                    # )
                else:
                    logging.error(f"Failed to download filings for ticker: {ticker}")
                    time.sleep(random.uniform(1, 2))
                    retry_counts[ticker] += 1
                    if retry_counts[ticker] < max_retries:
                        to_retry.add(ticker)

        time.sleep(1)

        for ticker, count in retry_counts.items():
            if count >= max_retries and ticker in to_retry:
                logging.error(f"Exceeded max retries for ticker {ticker}. Giving up.")


# Example usage
# ticker_list = ['AAPL', 'GOOG']
# download_filings_for_batch(ticker_list)
