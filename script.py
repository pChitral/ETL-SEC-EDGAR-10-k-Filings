import os
import json
import re
import pandas as pd
from bs4 import BeautifulSoup
from supabase import create_client
from shutil import rmtree
from dotenv import load_dotenv

from utils.get_ticker_10k_filings import get_ticker_10k_filings
from utils.collect_ticker_files import collect_ticker_files
from utils.new_10k_reports_to_supabase import new_10k_reports_to_supabase
from utils.delete_txt_files import delete_txt_files
from utils.parse_html_file import parse_html_file

# Supabase API keys
load_dotenv()
SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]
Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def process_ticker_10k_data(ticker):
    # Download 10-K filings
    try:
        get_ticker_10k_filings(ticker)
    except Exception as e:
        print(f"Error occurred while downloading filings for {ticker}: {e}")
        return {}

    ticker_files_dict = collect_ticker_files()

    # Delete .txt files to save space
    delete_txt_files(ticker_files_dict.get(ticker, []))

    # Initialize a dictionary to hold all parsed data
    all_parsed_data = {}

    # Loop through each HTML file to parse and store the data
    for html_file in ticker_files_dict.get(ticker, []):
        if html_file.endswith(".html"):
            path_parts = html_file.split("/")
            cik_year_acc = path_parts[4].split("-")

            if len(cik_year_acc) < 3:
                print(f"Skipping file with unexpected format: {html_file}")
                continue

            CIK, Year, AccessionNumber = cik_year_acc

            try:
                parsed_data = parse_html_file(html_file)
            except Exception as e:
                print(f"Could not parse {html_file} due to error: {e}")
                continue

            try:
                filing_dict = {
                    "ticker": ticker,
                    "cik": CIK,
                    "year": int(Year),
                    "accession_number": AccessionNumber,
                    "risk_factor": parsed_data["Risk Factors"],
                    "all_text": parsed_data["all_text"],
                }

            except ValueError:
                print(f"Skipping file with invalid year format in {html_file}")
                continue

            all_parsed_data[AccessionNumber] = filing_dict

    # Create a list of all parsed data dictionaries
    all_parsed_data_list = list(all_parsed_data.values())

    # Insert parsed data into Supabase
    new_10k_reports_to_supabase(all_parsed_data_list, Client)

    # Clear the data folder after processing
    if os.path.exists("data"):
        rmtree("data")

    return all_parsed_data


# Read the JSON file into a DataFrame
df = pd.read_json("company_tickers.json", orient="index")

# Process each ticker
all_tickers_data = {}
tickers = df["ticker"].tolist()

for ticker in tickers:
    all_tickers_data[ticker] = process_ticker_10k_data(ticker)
