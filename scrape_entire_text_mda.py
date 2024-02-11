# Standard library imports for concurrency, file operations, and data handling
import concurrent.futures
import os
import pandas as pd
import logging
import random
import time

from utils.processing.process_single_ticker import process_single_ticker

from utils.helpers.log_memory_usage import log_memory_usage
from utils.helpers.download_filings_for_batch import download_filings_for_batch
from utils.helpers.main_helpers import setup_logging
from utils.helpers.main_helpers import get_optimal_thread_count
from utils.helpers.main_helpers import update_processed_status

# Constants
TICKER_DATA_DIR = "ticker_data"
BATCH_SIZE = 5


if __name__ == "__main__":
    setup_logging()

    status_df = pd.read_csv("processing_status.csv")

    logging.info("Starting the processing of tickers.")

    to_process_df = status_df[~status_df["processed"]]

    total_tickers = len(to_process_df)
    processed_tickers_count = 0

    for batch_start in range(0, total_tickers, BATCH_SIZE):

        log_memory_usage()

        time.sleep(random.uniform(0.1, 0.9))

        batch_end = min(batch_start + BATCH_SIZE, total_tickers)
        tickers_batch = to_process_df.iloc[batch_start:batch_end]
        ticker_list = tickers_batch["ticker"].tolist()

        download_filings_for_batch(ticker_list)

        THREAD_COUNT = get_optimal_thread_count()

        processed_tickers = []

        with concurrent.futures.ThreadPoolExecutor(
            max_workers=THREAD_COUNT
        ) as executor:
            futures = {
                executor.submit(
                    process_single_ticker, row["ticker"], row["cik_str"], row["title"]
                ): row["ticker"]
                for _, row in tickers_batch.iterrows()
            }

            for future in concurrent.futures.as_completed(futures):

                try:
                    result, cik, ticker = future.result()

                    if result is not None and not result.empty:

                        os.makedirs(TICKER_DATA_DIR, exist_ok=True)
                        result.to_csv(f"{TICKER_DATA_DIR}/{ticker}.csv", index=False)

                        logging.info(f"Processed ticker: {ticker}")
                        processed_tickers.append(ticker)

                except Exception as e:
                    logging.error(f"Error processing ticker {futures[future]}: {e}")

        status_df = update_processed_status(status_df, processed_tickers)

        processed_tickers_count += len(processed_tickers)
        processed_percentage = (processed_tickers_count / total_tickers) * 100

        logging.info(
            f"Completed {processed_percentage:.2f}% (Processed {processed_tickers_count} of {total_tickers} tickers)"
        )

    status_df.to_csv("processing_status.csv", index=False)
    log_memory_usage()

    logging.info("All ticker data processed and exported.")
