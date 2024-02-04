import pandas as pd

WORD_LIST = None


def load_word_list():
    global WORD_LIST
    if WORD_LIST is None:
        word_list_df = pd.read_csv("updated_word_list.csv")  # Adjust path if necessary
        WORD_LIST = set(word_list_df["words"].tolist())
