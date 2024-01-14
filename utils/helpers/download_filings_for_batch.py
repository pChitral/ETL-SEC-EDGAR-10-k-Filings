from concurrent.futures import ThreadPoolExecutor, as_completed
from utils.get_ticker_10k_filings import get_ticker_10k_filings
import logging
from requests.exceptions import HTTPError
import time
import threading

# Semaphore to limit the number of requests to 10 per second
request_semaphore = threading.Semaphore(10)


def download_filings(cik):
    with request_semaphore:
        try:
            # Call the function to download filings for one CIK
            success = get_ticker_10k_filings(cik)
            return success
        except Exception as e:
            logging.error(
                f"Error occurred while downloading filings for CIK {cik}: {e}"
            )
            return None


def download_filings_for_batch(cik_list, max_retries=3):
    retry_counts = {cik: 0 for cik in cik_list}
    to_retry = set(cik_list)

    while to_retry:
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_cik = {
                executor.submit(download_filings, cik): cik for cik in to_retry
            }
            to_retry.clear()

            for future in as_completed(future_to_cik):
                cik = future_to_cik[future]
                success = future.result()
                if success:
                    logging.info(f"Successfully downloaded filings for CIK: {cik}")
                else:
                    logging.error(f"Failed to download filings for CIK: {cik}")
                    retry_counts[cik] += 1
                    if retry_counts[cik] < max_retries:
                        to_retry.add(cik)

            # Throttle requests to respect the rate limit
            time.sleep(1)

        for cik, count in retry_counts.items():
            if count >= max_retries and cik in to_retry:
                logging.error(
                    f"Exceeded max retries for CIK {cik}. Giving up on this CIK."
                )
                to_retry.remove(cik)


# Example use:
# cik_list = ['0000320193', '0000789019']
# download_filings_for_batch(cik_list)
