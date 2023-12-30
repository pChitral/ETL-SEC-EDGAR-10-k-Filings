from utils.extract_mda_section import extract_mda_section
from utils.get_word_frequencies import get_word_frequencies


def parse_html_file_mda(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    mda_section = extract_mda_section(file_path)  # Use the updated function
    return mda_section
    # return {
    #     "MD&A": mda_section if mda_section else "MD&A section not found",
    #     "target_word_frequency": get_word_frequencies(mda_section),
    # }
