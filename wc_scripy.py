import os
import pandas as pd
from bs4 import BeautifulSoup
from supabase import create_client
from dotenv import load_dotenv
from collections import Counter
import json
from utils.get_ticker_10k_filings import get_ticker_10k_filings
from utils.collect_ticker_files import collect_ticker_files
from utils.delete_txt_files import delete_txt_files
from shutil import rmtree
import re

# Supabase API keys
load_dotenv()
SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]
Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def extract_mda_section(file_path: str) -> str:
    """
    Extract the "Management’s Discussion and Analysis of Financial Condition and Results of Operations"
    section from a 10-K report HTML file by first parsing the HTML content.

    Args:
    - file_path (str): Path to the HTML file of the 10-K report.

    Returns:
    - str: Text of the MDA section.
    """
    # Load and parse the HTML file content
    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file.read(), "html.parser")

    # Convert the parsed content to text and lowercase it
    parsed_text = soup.get_text()
    lower_parsed_text = parsed_text.lower()

    # Using a regex pattern to find all occurrences of "item 7." and "item 8."
    item_7_matches = [
        match.start() for match in re.finditer(r"item\s*7\.", lower_parsed_text)
    ]
    item_8_matches = [
        match.start() for match in re.finditer(r"item\s*8\.", lower_parsed_text)
    ]

    # If we have less than 2 occurrences of "item 7.", return section not found
    if len(item_7_matches) < 2:
        return "MD&A section not found."

    # Extract content between the second occurrence of "item 7." and the occurrence of "item 8." after that
    section_content = parsed_text[item_7_matches[1] : item_8_matches[1]].strip()

    return section_content


def find_general_section(section_title, text):
    start = text.find(section_title)
    if start == -1:
        return None
    end = text.find("ITEM", start + 1)
    if end == -1:
        end = None
    return text[start:end].strip()


# Read the words from the provided file
with open("words_fraud_constraints.json", "r") as file:
    target_words = json.load(file)


def get_word_frequencies(text):
    words = text.split()
    frequency = Counter(words)
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


def new_10k_reports_to_supabase(parsed_data_list, client):
    for data in parsed_data_list:
        response = client.table("reports_10k").insert(data).execute()


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
    if count > 3:
        break
