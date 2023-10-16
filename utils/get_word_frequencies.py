from collections import Counter
import json

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
    target_frequencies = {word: frequency.get(word, 0) for word in target_words}

    return json.dumps(target_frequencies)
