import multiprocessing
import os
import pandas as pd
import logging
from utils.processing.process_single_ticker import process_single_ticker
from utils.helpers.log_memory_usage import log_memory_usage
from utils.helpers.download_filings_for_batch import download_filings_for_batch

# Constants
TICKER_DATA_DIR = "ticker_data"
BATCH_SIZE = 8
LOG_FILE = "ticker_processing.log"


# Setup basic configuration for logging
def setup_logging():
    if not logging.getLogger().hasHandlers():
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()],
        )


def update_processed_status(status_df, processed_tickers):
    """Bulk update of processed tickers to improve efficiency."""
    mask = status_df["ticker"].isin(processed_tickers)
    status_df.loc[mask, "processed"] = True
    return status_df


def worker_process(ticker_info):
    """Wrapper function for process_single_ticker with error handling."""
    try:
        result = process_single_ticker(*ticker_info)
        if (
            result is not None and not result[0].empty
        ):  # Assuming the first item in the tuple is the DataFrame
            return result
    except Exception as e:
        logging.error(f"Error processing ticker {ticker_info[0]}: {str(e)}")
    return None


if __name__ == "__main__":
    setup_logging()
    status_df = pd.read_csv("processing_status.csv")
    logging.info("Starting the processing of tickers.")

    to_process_df = status_df[~status_df["processed"]]
    processed_tickers = []

    for batch_start in range(0, len(to_process_df), BATCH_SIZE):
        log_memory_usage()
        batch_end = min(batch_start + BATCH_SIZE, len(to_process_df))
        tickers_batch = to_process_df.iloc[batch_start:batch_end]
        ticker_data = [
            (row["ticker"], row["cik_str"], row["title"])
            for _, row in tickers_batch.iterrows()
        ]

        with multiprocessing.Pool(processes=BATCH_SIZE) as pool:
            results = pool.map(worker_process, ticker_data)

        for result in results:
            if result:
                df, cik, ticker = result  # Unpack the result tuple
                os.makedirs(TICKER_DATA_DIR, exist_ok=True)
                df.to_csv(f"{TICKER_DATA_DIR}/{ticker}.csv", index=False)
                logging.info(f"Processed ticker: {ticker}")
                processed_tickers.append(ticker)

        status_df = update_processed_status(status_df, processed_tickers)

    processed_percentage = (len(processed_tickers) / len(to_process_df)) * 100
    logging.info(
        f"Completed {processed_percentage:.2f}% (Processed {len(processed_tickers)} of {len(to_process_df)} tickers)"
    )
    status_df.to_csv("processing_status.csv", index=False)
    log_memory_usage()
    logging.info("All ticker data processed and exported.")
