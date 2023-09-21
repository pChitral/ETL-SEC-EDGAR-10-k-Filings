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

# Supabase API keys
load_dotenv()
SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]
Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# Function to insert parsed data into Supabase
def new_10k_reports_to_supabase(all_parsed_data_list, Client):
    try:
        parsed_data_df = pd.DataFrame(all_parsed_data_list)
        existing_reports_in_supabase = Client.table("reports_10k").select("*").execute()

        if existing_reports_in_supabase.data:
            existing_accession_numbers = [
                record["accession_number"]
                for record in existing_reports_in_supabase.data
            ]
        else:
            existing_accession_numbers = []

        filtered_reports_df = parsed_data_df[
            ~parsed_data_df["accession_number"].isin(existing_accession_numbers)
        ]
        formatted_filtered_reports = filtered_reports_df.to_dict(orient="records")
        data_reports = (
            Client.table("reports_10k").insert(formatted_filtered_reports).execute()
        )

        assert len(data_reports.data) > 0, "No reports were embedded successfully."
        return data_reports.data

    except Exception as e:
        return f"An error occurred during embedding: {e}"


def find_general_section(title, text_content):
    sections = re.split(r"Item\s+\d+", text_content)
    for section in sections:
        if re.search(re.escape(title), section, re.IGNORECASE):
            return section.strip()
    return None


def delete_txt_files(files):
    for file in files:
        if file.endswith(".txt"):
            os.remove(file)


def parse_html_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file.read(), "lxml")
    all_text = " ".join([tag.strip() for tag in soup.stripped_strings])
    risk_factors_section = find_general_section("Risk Factors", all_text)
    parsed_data = {
        "Risk Factors": risk_factors_section
        if risk_factors_section
        else "Section not found"
    }
    return parsed_data


def process_ticker_10k_data(ticker):
    # Download 10-K filings
    get_ticker_10k_filings(ticker)
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
                    "parsed_data": json.dumps(parsed_data),
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
    rmtree("data")

    return all_parsed_data


# Example usage
# Replace with your loop over tickers
all_tickers_data = {}
tickers = ["AAPL", "GOOG"]  # Add your list of tickers here

for ticker in tickers:
    all_tickers_data[ticker] = process_ticker_10k_data(ticker)

