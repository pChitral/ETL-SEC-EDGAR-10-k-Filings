import pandas as pd
from bs4 import BeautifulSoup
import json


def extract_word_count(html_file_path: str) -> str:
    """
    Extracts the count of predefined words from the text in an HTML file.

    Args:
    - html_file_path (str): The file path of the HTML file to be analyzed.

    Returns:
    - str: A JSON object (as a string) containing the word counts.
    """
    # Step 1: Adjust the path to read the word list from the CSV file
    word_list_df = pd.read_csv("updated_word_list.csv")  # Adjusted path
    word_list = word_list_df["words"].tolist()

    # Step 2: Parse the HTML file to extract text
    with open(html_file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")
        text = soup.get_text(separator=" ", strip=True)

    # Step 3: Count occurrences of each word
    word_counts = {word: text.count(word) for word in word_list}

    # Step 4: Convert the word counts to a JSON object
    word_counts_json = json.dumps(word_counts)

    return word_counts_json
