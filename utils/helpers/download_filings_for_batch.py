from concurrent.futures import ThreadPoolExecutor, as_completed
from utils.get_ticker_10k_filings import get_ticker_10k_filings
import logging
from requests.exceptions import HTTPError
import time
import threading

# Semaphore to limit the number of requests to 10 per second
request_semaphore = threading.Semaphore(10)


def download_filings(ticker):
    with request_semaphore:
        try:
            # Call the function to download filings for one ticker
            success = get_ticker_10k_filings(ticker)
            return success
        except Exception as e:
            logging.error(
                f"Error occurred while downloading filings for ticker {ticker}: {e}"
            )
            return None


def download_filings_for_batch(ticker_list, max_retries=3):
    retry_counts = {ticker: 0 for ticker in ticker_list}
    to_retry = set(ticker_list)

    while to_retry:
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_cik = {
                executor.submit(download_filings, ticker): ticker for ticker in to_retry
            }
            to_retry.clear()

            for future in as_completed(future_to_cik):
                ticker = future_to_cik[future]
                success = future.result()
                if success:
                    logging.info(f"Successfully downloaded filings for ticker: {ticker}")
                else:
                    logging.error(f"Failed to download filings for ticker: {ticker}")
                    retry_counts[ticker] += 1
                    if retry_counts[ticker] < max_retries:
                        to_retry.add(ticker)

            # Throttle requests to respect the rate limit
            time.sleep(1)

        for ticker, count in retry_counts.items():
            if count >= max_retries and ticker in to_retry:
                logging.error(
                    f"Exceeded max retries for ticker {ticker}. Giving up on this ticker."
                )
                to_retry.remove(ticker)


# Example use:
# ticker_list = ['AAPL', 'GOOG']
# download_filings_for_batch(ticker_list)
