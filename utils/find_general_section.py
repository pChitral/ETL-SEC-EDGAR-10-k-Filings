import re


def find_general_section(title, text_content):
    sections = re.split(r"Item\s+\d+", text_content)
    for section in sections:
        if re.search(re.escape(title), section, re.IGNORECASE):
            return section.strip()
    return None
