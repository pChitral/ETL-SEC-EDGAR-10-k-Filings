"""
This module contains a function to extract the "Management’s Discussion and Analysis of Financial
Condition and Results of Operations" (MD&A) section from an SEC 10-K report HTML file.
"""

import re
from typing import Optional
from bs4 import BeautifulSoup

ITEM_7_PATTERN: re.Pattern = re.compile(r"item\s*7\.")
ITEM_8_PATTERN: re.Pattern = re.compile(r"item\s*8\.")


def extract_mda_section(file_path: str) -> Optional[str]:
    """
    Extracts the "Management’s Discussion and Analysis of Financial Condition and Results of Operations"
    (MD&A) section from an SEC 10-K report HTML file. This function parses the HTML content to find
    and return the text between the headings "Item 7" and "Item 8."

    Args:
        file_path (str): The file path to the 10-K report HTML file.

    Returns:
        Optional[str]: The cleaned text of the MD&A section if found; otherwise, a message indicating
        that the MD&A section was not found.

    Raises:
        FileNotFoundError: If the specified file path does not exist or is inaccessible.
        UnicodeDecodeError: If there is an error in decoding the file's content.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            soup = BeautifulSoup(file.read(), "html.parser")
    except (FileNotFoundError, UnicodeDecodeError) as e:
        raise e

    parsed_text: str = soup.get_text()
    lower_parsed_text: str = parsed_text.lower()

    item_7_matches = [
        match.start() for match in ITEM_7_PATTERN.finditer(lower_parsed_text)
    ]
    item_8_matches = [
        match.start() for match in ITEM_8_PATTERN.finditer(lower_parsed_text)
    ]

    if not item_7_matches or not item_8_matches:
        return "MD&A section not found."

    start_idx = item_7_matches[1] if len(item_7_matches) > 1 else item_7_matches[0]
    end_idx = item_8_matches[1] if len(item_8_matches) > 1 else item_8_matches[0]

    section_content: str = parsed_text[start_idx:end_idx].strip()
    section_content = " ".join(section_content.split())
    section_content = BeautifulSoup(section_content, "html.parser").get_text()

    return section_content
