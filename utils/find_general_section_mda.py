def find_general_section(section_title, text):
    start = text.find(section_title)
    if start == -1:
        return None
    end = text.find("ITEM", start + 1)
    if end == -1:
        end = None
    return text[start:end].strip()
    