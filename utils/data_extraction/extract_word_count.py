import pandas as pd
from bs4 import BeautifulSoup
import json
from collections import Counter
import re


def extract_word_count(html_file_path: str) -> str:
    """
    Extracts the count of predefined words from the text in an HTML file.

    Args:
    - html_file_path (str): The file path of the HTML file to be analyzed.

    Returns:
    - str: A JSON object (as a string) containing the word counts.
    """
    # Load the word list from the CSV file
    try:
        word_list_df = pd.read_csv("updated_word_list.csv")
    except FileNotFoundError:
        return json.dumps({"error": "Word list file not found."})

    word_list = set(word_list_df["words"].tolist())

    # Parse the HTML file to extract text
    try:
        with open(html_file_path, "r", encoding="utf-8") as file:
            soup = BeautifulSoup(file, "html.parser")
    except (FileNotFoundError, UnicodeDecodeError) as e:
        return json.dumps({"error": str(e)})

    text = soup.get_text(" ", strip=True).lower()
    words_in_text = re.findall(r"\b\w+\b", text)

    # Count occurrences of each word efficiently
    word_counts = Counter(words_in_text)
    selected_word_counts = {
        word: word_counts[word] for word in word_list if word in word_counts
    }

    # Convert the word counts to a JSON object
    return json.dumps(selected_word_counts)
