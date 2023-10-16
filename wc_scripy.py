import os
import pandas as pd

from supabase import create_client
from dotenv import load_dotenv
from collections import Counter
import json
from utils.get_ticker_10k_filings import get_ticker_10k_filings
from utils.collect_ticker_files import collect_ticker_files
from utils.delete_txt_files import delete_txt_files
from shutil import rmtree
from collections import Counter
import json
from utils.extract_mda_section import extract_mda_section

# Supabase API keys
load_dotenv()
SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]
Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# Load the JSON file
with open("words_fraud_constraints.json", "r") as file:
    data = json.load(file)
# Combine the fraud and constraints words into a single list
target_words = set(data["fraud"] + data["constraints"])


def get_word_frequencies(text):
    """
    Get the frequency of target words related to "fraud" and "constraints" in a given text.

    Parameters:
    - text (str): The input text in which to search for the target words.

    Returns:
    - str: A JSON-formatted string containing the frequencies of the target words found in the text.
    """

    # Split the text into individual words
    words = text.split()

    # Calculate word frequencies for the entire text
    frequency = Counter(words)

    # Extract frequencies of the target words
    target_frequencies = {
        word: frequency[word] for word in target_words if word in frequency
    }

    return json.dumps(target_frequencies)


def parse_html_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    mda_section = extract_mda_section(file_path)  # Use the updated function
    return {
        "MD&A": mda_section if mda_section else "MD&A section not found",
        "target_word_frequency": get_word_frequencies(mda_section),
    }


def new_10k_reports_to_supabase(all_parsed_data_list, Client):
    try:
        # Convert the parsed data list to a DataFrame
        parsed_data_df = pd.DataFrame(all_parsed_data_list)

        # Fetch the existing reports from Supabase
        existing_reports_in_supabase = Client.table("reports_10k").select("*").execute()

        # Check if data exists and get the accession numbers
        if existing_reports_in_supabase.data:
            existing_accession_numbers = [
                record["accession_number"]
                for record in existing_reports_in_supabase.data
            ]
        else:
            existing_accession_numbers = []

        # Filter out the reports that are already in the database
        filtered_reports_df = parsed_data_df[
            ~parsed_data_df["accession_number"].isin(existing_accession_numbers)
        ]
        formatted_filtered_reports = filtered_reports_df.to_dict(orient="records")

        # Insert the new data into the reports_10k table
        if formatted_filtered_reports:
            data_reports = (
                Client.table("reports_10k").insert(formatted_filtered_reports).execute()
            )

            # Handle any errors during the insertion process
            if data_reports.error:
                print(f"Supabase Error: {data_reports.error}")

            assert len(data_reports.data) > 0, "No reports were embedded successfully."
            return data_reports.data

        else:
            print("No new reports to add.")
            return []

    except Exception as e:
        print(f"An error occurred during embedding: {e}")
        return []


def process_ticker_10k_data(ticker):
    try:
        get_ticker_10k_filings(ticker)
    except Exception as e:
        print(f"Error occurred while downloading filings for {ticker}: {e}")
        return {}

    ticker_files_dict = collect_ticker_files()
    delete_txt_files(ticker_files_dict.get(ticker, []))

    all_parsed_data = {}
    for html_file in ticker_files_dict.get(ticker, []):
        if html_file.endswith(".html"):
            path_parts = html_file.split("/")
            cik_year_acc = path_parts[4].split("-")

            if len(cik_year_acc) < 3:
                print(f"Skipping file with unexpected format: {html_file}")
                continue

            CIK = cik_year_acc[0]
            # Convert the two-digit year to four digits
            two_digit_year = cik_year_acc[1]
            if (
                int(two_digit_year) > 50
            ):  # Assuming we're starting from 1950 for simplicity
                Year = "19" + two_digit_year
            else:
                Year = "20" + two_digit_year
            AccessionNumber = cik_year_acc[2]
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
                    "mda_section": parsed_data.get("MD&A", "Section not found"),
                    "target_word_frequency": parsed_data.get("word_frequency", "{}"),
                }
            except ValueError:
                print(f"Skipping file with invalid year format in {html_file}")
                continue

            all_parsed_data[AccessionNumber] = filing_dict

    all_parsed_data_list = list(all_parsed_data.values())
    new_10k_reports_to_supabase(all_parsed_data_list, Client)
    # Clear the data folder after processing
    if os.path.exists("data"):
        rmtree("data")
    return all_parsed_data


df = pd.read_json("company_tickers.json", orient="index")
all_tickers_data = {}
tickers = df["ticker"].tolist()
count = 0
for ticker in tickers:
    all_tickers_data[ticker] = process_ticker_10k_data(ticker)
    count += 1
    if count > 100:
        break
