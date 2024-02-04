from utils.data_extraction.extract_word_count import extract_word_count

import logging

from datetime import datetime


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
            logging.warning(f"Skipping file with unexpected date format: {html_file}")
            return None

        two_digit_year = cik_year_acc[1]
        Year = (
            "19" + two_digit_year if int(two_digit_year) > 50 else "20" + two_digit_year
        )

        try:
            parsed_data = extract_word_count(html_file)
            filing_dict = {
                "cik": cik,
                "ticker": ticker,
                "title": title,
                "year": int(Year),
                "word_count": parsed_data,
                "processed_timestamp": datetime.now(),
            }
            return filing_dict
        except Exception as e:
            logging.error(f"Could not parse {html_file} due to error: {e}")
            return None
