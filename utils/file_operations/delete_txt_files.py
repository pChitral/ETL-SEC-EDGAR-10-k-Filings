import os
from typing import List


def delete_txt_files(files: List[str]) -> None:
    """
    Deletes all files with a '.txt' extension from a list of file names.

    Parameters:
        files (List[str]): A list of file names (strings) to be checked and deleted if they end with '.txt'.

    Returns:
        None: This function does not return anything. It performs a deletion operation on files.
    """
    txt_files = [file for file in files if file.endswith(".txt")]
    for file in txt_files:
        os.remove(file)
