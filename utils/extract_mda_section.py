from bs4 import BeautifulSoup
import re

ITEM_7_PATTERN = re.compile(r"item\s*7\.")
ITEM_8_PATTERN = re.compile(r"item\s*8\.")


def extract_mda_section(file_path: str) -> str:
    """
    Extract the "Management’s Discussion and Analysis of Financial Condition and Results of Operations"
    section from a 10-K report HTML file by first parsing the HTML content.

    Args:
    - file_path (str): Path to the HTML file of the 10-K report.

    Returns:
    - str: Cleaned text of the MDA section.
    """
    # Load and parse the HTML file content
    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file.read(), "html.parser")

    # Convert the parsed content to text and lowercase it
    parsed_text = soup.get_text()
    lower_parsed_text = parsed_text.lower()

    # Using the precompiled regex patterns to find all occurrences of "item 7." and "item 8."
    item_7_matches = [
        match.start() for match in ITEM_7_PATTERN.finditer(lower_parsed_text)
    ]
    item_8_matches = [
        match.start() for match in ITEM_8_PATTERN.finditer(lower_parsed_text)
    ]

    # If we don't have any occurrence of "item 7." or "item 8.", return section not found
    if not item_7_matches or not item_8_matches:
        return "MD&A section not found."

    # Choose the starting point based on the number of occurrences of "item 7."
    start_idx = item_7_matches[1] if len(item_7_matches) > 1 else item_7_matches[0]

    # Choose the ending point based on the number of occurrences of "item 8."
    end_idx = item_8_matches[1] if len(item_8_matches) > 1 else item_8_matches[0]

    # Extract content between the chosen "item 7." occurrence and the chosen "item 8." occurrence
    section_content = parsed_text[start_idx:end_idx].strip()

    # Cleanup: Remove extra whitespace, newlines, and HTML entities
    section_content = " ".join(section_content.split())
    section_content = BeautifulSoup(section_content, "html.parser").get_text()

    return section_content
