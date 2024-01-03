# Standard library imports for concurrency, file operations, and data handling
import concurrent.futures
import os
import pandas as pd
import logging
import random
import time

# Utility functions from the utils module for specific operations
from utils.helpers.initialize_status_file import initialize_status_file
from utils.helpers.update_status_file import update_status_file
from utils.processing.process_single_ticker import process_single_ticker
from utils.helpers.write_to_master_file import write_to_master_file

# File locking mechanism to handle concurrent writes to a file
from filelock import FileLock

# Set up basic configuration for logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("ticker_processing.log"), logging.StreamHandler()],
)

# Define the batch size for processing tickers
BATCH_SIZE = 9

if __name__ == "__main__":
    # Load company tickers data from a JSON file
    df = pd.read_json("company_tickers.json", orient="index")

    # Initialize the status file to keep track of processed tickers
    initialize_status_file(df)
    status_df = pd.read_csv("processing_status.csv")

    logging.info("Starting the processing of tickers.")

    # Set the total number of tickers to process
    total_tickers = len(df)
    all_tickers_data = []

    # Loop through tickers in batches for processing
    for batch_start in range(0, total_tickers, BATCH_SIZE):
        # Introduce a random sleep time between batches
        sleep_time = random.uniform(1, 2)
        time.sleep(sleep_time)

        # Determine the end of the current batch
        batch_end = min(batch_start + BATCH_SIZE, total_tickers)
        tickers_batch = df.iloc[batch_start:batch_end]

        # Process tickers in the current batch concurrently
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for index, row in tickers_batch.iterrows():
                # Check if the ticker has already been processed
                if not status_df.loc[
                    status_df["ticker"] == row["ticker"], "processed"
                ].any():
                    # Submit ticker processing jobs to the executor
                    futures.append(
                        executor.submit(
                            process_single_ticker,
                            row["ticker"],
                            row["cik_str"],
                            row["title"],
                        )
                    )

            # Collect results from futures as they complete
            for future in concurrent.futures.as_completed(futures):
                result, cik, ticker = future.result()
                if result is not None and not result.empty:
                    # Create directory for ticker data if it doesn't exist
                    os.makedirs("ticker_data", exist_ok=True)
                    # Save the processed data to a CSV file
                    result.to_csv(f"ticker_data/{ticker}.csv", index=False)
                    all_tickers_data.append(result)
                    # Log the processing of the ticker
                    logging.info(f"Processed ticker: {ticker}")
                    # Update the status file to mark the ticker as processed
                    update_status_file(ticker)

        # Log the percentage of tickers processed so far
        processed_percentage = (batch_end / total_tickers) * 100
        logging.info(
            f"Completed {processed_percentage:.2f}% (Processed {batch_end} of {total_tickers} tickers)"
        )

    # Concatenate all processed data and write to a master file
    if all_tickers_data:
        master_df = pd.concat(all_tickers_data, ignore_index=True)
        write_to_master_file(master_df)

    # Log completion of data processing
    logging.info("All ticker data processed and exported.")
