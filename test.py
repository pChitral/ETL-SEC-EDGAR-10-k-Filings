import concurrent.futures
from utils.get_ticker_10k_filings import get_ticker_10k_filings
from utils.collect_ticker_files import collect_ticker_files
from utils.delete_txt_files import delete_txt_files
from utils.parse_html_file_mda import parse_html_file_mda
import os
import pandas as pd


# New Function: Process a single HTML file
def process_html_file(html_file, ticker):
    if html_file.endswith(".html"):
        path_parts = html_file.split("/")
        cik_year_acc = path_parts[4].split("-")

        if len(cik_year_acc) < 3:
            print(f"Skipping file with unexpected format: {html_file}")
            return None

        CIK = cik_year_acc[0]
        # Convert the two-digit year to four digits
        two_digit_year = cik_year_acc[1]
        Year = (
            "19" + two_digit_year if int(two_digit_year) > 50 else "20" + two_digit_year
        )
        AccessionNumber = cik_year_acc[2]

        try:
            parsed_data = parse_html_file_mda(html_file)
            filing_dict = {
                "ticker": ticker,
                "cik": CIK,
                "year": int(Year),
                "accession_number": AccessionNumber,
                "mda_section": parsed_data,
            }
            return filing_dict
        except Exception as e:
            print(f"Could not parse {html_file} due to error: {e}")
            return None


# Modified Function: Process ticker 10-K data with parallel processing
def process_ticker_10k_data(ticker):
    try:
        get_ticker_10k_filings(ticker)
    except Exception as e:
        print(f"Error occurred while downloading filings for {ticker}: {e}")
        return {}

    ticker_files_dict = collect_ticker_files()
    delete_txt_files(ticker_files_dict.get(ticker, []))

    # Parallel processing of HTML files
    html_files = ticker_files_dict.get(ticker, [])
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(lambda file: process_html_file(file, ticker), html_files)
        all_parsed_data = {
            result["accession_number"]: result
            for result in results
            if result is not None
        }

    # Create a list of all parsed data dictionaries
    all_parsed_data_list = list(all_parsed_data.values())

    return all_parsed_data_list


# Read the JSON file into a DataFrame
df = pd.read_json("company_tickers.json", orient="index")
# Example usage

all_tickers_data = {}
tickers = df["ticker"].tolist()
count = 0
for ticker in tickers:
    all_tickers_data[ticker] = process_ticker_10k_data(ticker)
    count += 1
    if count > 1:
        break

# Convert the dictionary to a DataFrame first if needed
result_df = pd.DataFrame.from_dict(all_tickers_data, orient="index")

# Save to JSON
result_df.to_json("output_file.json", orient="index", indent=4)
