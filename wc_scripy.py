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

# Supabase API keys
load_dotenv()
SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]
Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def extract_mdna_section(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    soup = BeautifulSoup(content, "html.parser")

    item_7_variants = ["ITEM 7.", "ITEM 7 –", "ITEM 7—"]
    mda_start = None
    for variant in item_7_variants:
        mda_start = soup.find(string=lambda text: variant in text)
        if mda_start:
            break

    if not mda_start:
        return "MD&A section not found."

    mda_content = []
    for sibling in mda_start.find_all_next(string=True):
        if sibling and "ITEM 8." in sibling:
            break
        if sibling:  # Check if sibling is not None
            mda_content.append(sibling.strip())

    refined_mda_content = []
    for item in mda_content:
        if "PAGE" in item or "Table of Contents" in item or "Part II" in item:
            continue
        refined_mda_content.append(item)

    mdna_text = " ".join(refined_mda_content)
    mdna_text = " ".join(mdna_text.split())

    unwanted_patterns = ["&nbsp;", "&#146;", "&#147;", "&#148;"]
    for pattern in unwanted_patterns:
        mdna_text = mdna_text.replace(pattern, "")

    return mdna_text


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
    mda_section = find_general_section("ITEM 7.", content)
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
