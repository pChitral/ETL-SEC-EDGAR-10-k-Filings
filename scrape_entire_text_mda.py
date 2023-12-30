import concurrent.futures
from datetime import datetime
import os
import pandas as pd
import logging
from utils.get_ticker_10k_filings import get_ticker_10k_filings
from utils.collect_ticker_files import collect_ticker_files
from utils.delete_txt_files import delete_txt_files
from utils.parse_html_file_mda import parse_html_file_mda

# Set up basic configuration for logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("ticker_processing.log"), logging.StreamHandler()],
)


def process_html_file(html_file, ticker, cik, title):
    """
    Process a single HTML file to extract the Management Discussion and Analysis (MDA) section.

    Args:
    - html_file (str): Path to the HTML file.
    - ticker (str): Ticker symbol of the company.

    Returns:
    - dict: A dictionary containing the ticker, year, MDA section, and processed timestamp.
            Returns None if the file cannot be processed.
    """
    if html_file.endswith(".html"):
        path_parts = html_file.split("/")
        cik_year_acc = path_parts[4].split("-")

        if len(cik_year_acc) < 3:
            logging.warning(f"Skipping file with unexpected format: {html_file}")
            return None

        two_digit_year = cik_year_acc[1]
        Year = (
            "19" + two_digit_year if int(two_digit_year) > 50 else "20" + two_digit_year
        )

        try:
            parsed_data = parse_html_file_mda(html_file)
            filing_dict = {
                "cik": cik,
                "ticker": ticker,
                "title": title,
                "year": int(Year),
                "mda_section": parsed_data,
                "processed_timestamp": datetime.now(),
            }
            return filing_dict
        except Exception as e:
            logging.error(f"Could not parse {html_file} due to error: {e}")
            return None


def process_ticker_10k_data(ticker, cik, title):
    """
    Process the 10-K filings for a given ticker.

    Args:
    - ticker (str): Ticker symbol of the company.

    Returns:
    - list: A list of dictionaries containing the parsed data for each 10-K filing.
    """
    # Attempt to download the filings, and check if it was successful
    if not get_ticker_10k_filings(ticker):
        logging.info(f"Failed to download filings for {ticker}. Skipping processing.")
        return []

    ticker_files_dict = collect_ticker_files()
    delete_txt_files(ticker_files_dict.get(ticker, []))

    html_files = ticker_files_dict.get(ticker, [])
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(
            lambda file: process_html_file(file, ticker, cik, title), html_files
        )
        all_parsed_data = {
            result["processed_timestamp"]: result
            for result in results
            if result is not None
        }

    all_parsed_data_list = list(all_parsed_data.values())
    logging.info(
        f"Completed processing {len(all_parsed_data_list)} HTML files for {ticker}"
    )
    return all_parsed_data_list


def process_single_ticker(ticker, cik, title):
    """
    Process a single ticker's 10-K filings.
    """
    ticker_data = process_ticker_10k_data(ticker, cik, title)
    if ticker_data:
        ticker_df = pd.DataFrame(ticker_data)
        logging.info(f"Processed {len(ticker_df)} 10-K filings for {ticker}")
        return ticker_df
    else:
        logging.info(f"No data to process for ticker: {ticker}")
        return pd.DataFrame()


BATCH_SIZE = 10  # Define the batch size

# Main script execution
if __name__ == "__main__":
    df = pd.read_json("company_tickers.json", orient="index")
    logging.info("Starting the processing of tickers.")
    total_tickers = 20
    # total_tickers = len(df)

    for batch_start in range(0, total_tickers, BATCH_SIZE):
        batch_end = min(batch_start + BATCH_SIZE, total_tickers)
        tickers_batch = df.iloc[batch_start:batch_end]

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(
                    process_single_ticker, row["ticker"], row["cik_str"], row["title"]
                )
                for index, row in tickers_batch.iterrows()
            ]
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result is not None and not result.empty:
                    result.to_csv(
                        "tickers_10k_data.csv",
                        mode="a",
                        header=not os.path.exists("tickers_10k_data.csv"),
                        index=False,
                    )
                    logging.info(
                        f"Processed ticker: {result['ticker'].iloc[0]} (Row {batch_start})"
                    )
                else:
                    logging.info(f"Empty DataFrame for ticker: {row['ticker']}")

        processed_percentage = (batch_end / total_tickers) * 100
        logging.info(
            f"Completed {processed_percentage:.2f}% (Processed {batch_end} of {total_tickers} tickers)"
        )

    logging.info("All ticker data processed and exported.")
