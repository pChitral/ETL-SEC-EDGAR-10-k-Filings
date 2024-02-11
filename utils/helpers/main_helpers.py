import os
import logging
LOG_FILE = "ticker_processing.log"

def get_optimal_thread_count():
    """Dynamically determine the optimal number of threads."""
    cpu_cores = os.cpu_count()
    return max(1, int(cpu_cores * 0.75))


def update_processed_status(status_df, processed_tickers):
    """Bulk update of processed tickers to improve efficiency."""
    mask = status_df["ticker"].isin(processed_tickers)
    status_df.loc[mask, "processed"] = True
    return status_df


# Set up basic configuration for logging
def setup_logging():
    if not logging.getLogger().hasHandlers():
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()],
        )
