from concurrent.futures import ThreadPoolExecutor, as_completed
from utils.get_ticker_10k_filings import get_ticker_10k_filings
import logging
from requests.exceptions import HTTPError


def download_filings_for_batch(cik_list, max_retries=3):
    """
    Download 10-K filings for a batch of CIKs concurrently with retry logic.
    """
    retry_counts = {cik: 0 for cik in cik_list}
    to_retry = set(cik_list)

    while to_retry:
        with ThreadPoolExecutor(max_workers=5) as executor:
            # Submit jobs to the executor for each CIK
            future_to_cik = {
                executor.submit(get_ticker_10k_filings, cik): cik for cik in to_retry
            }
            to_retry.clear()

            for future in as_completed(future_to_cik):
                cik = future_to_cik[future]
                try:
                    success = future.result()
                    if success:
                        logging.info(f"Successfully downloaded filings for CIK: {cik}")
                    else:
                        raise RuntimeError(f"Download failed for CIK: {cik}")
                except HTTPError as e:
                    logging.error(f"HTTP error for CIK {cik}: {e}")
                    if e.response and e.response.status_code == 429:  # Rate limit error
                        logging.warning(
                            f"Rate limit exceeded for CIK {cik}. Will retry."
                        )
                        retry_counts[cik] += 1
                        if retry_counts[cik] < max_retries:
                            to_retry.add(cik)
                except Exception as e:
                    logging.error(f"General error occurred for CIK {cik}: {e}")
                    retry_counts[cik] += 1
                    if retry_counts[cik] < max_retries:
                        to_retry.add(cik)

        # Check if any CIKs have exceeded the max retry limit
        for cik, count in retry_counts.items():
            if count >= max_retries and cik in to_retry:
                logging.error(
                    f"Exceeded max retries for CIK {cik}. Giving up on this CIK."
                )
                to_retry.remove(cik)


# Example use:
# cik_list = ['0000320193', '0000789019']  # Replace with actual CIKs
# download_filings_for_batch(cik_list)
