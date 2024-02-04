import json
import re
from collections import Counter

import pandas as pd
from bs4 import BeautifulSoup


def extract_word_count(html_file_path: str) -> str:
    """
    Extracts the count of predefined words from the text in an HTML file and
    returns a JSON string with the word counts.

    The function reads a list of words from a CSV file named 'updated_word_list.csv',
    parses the given HTML file to extract all text, and then counts the occurrences
    of each word from the list in the extracted text.

    Args:
        html_file_path (str): The file path of the HTML file to be analyzed.

    Returns:
        str: A JSON string representing an object where each key is a word from
        the list and its value is the count of that word in the HTML text. If an
        error occurs (e.g., file not found), the JSON string will contain an
        'error' key with a description of the error.

    Raises:
        FileNotFoundError: If 'updated_word_list.csv' or the specified HTML file
        cannot be found.
        UnicodeDecodeError: If there's an encoding issue with the HTML file.
    """
    try:
        word_list_df = pd.read_csv("updated_word_list.csv")
    except FileNotFoundError as e:
        raise FileNotFoundError(
            "Word list file 'updated_word_list.csv' not found."
        ) from e

    word_list = set(word_list_df["words"].tolist())

    try:
        with open(html_file_path, "r", encoding="utf-8") as file:
            soup = BeautifulSoup(file, "html.parser")
    except FileNotFoundError as e:
        raise FileNotFoundError(f"HTML file '{html_file_path}' not found.") from e
    except UnicodeDecodeError as e:
        raise UnicodeDecodeError("Encoding issue with the HTML file.") from e

    text = soup.get_text(" ", strip=True).lower()
    words_in_text = re.findall(r"\b\w+\b", text)

    word_counts = Counter(words_in_text)
    selected_word_counts = {
        word: word_counts[word] for word in word_list if word in word_counts
    }

    return json.dumps(selected_word_counts)
