import os


def delete_txt_files(files):
    for file in files:
        if file.endswith(".txt"):
            os.remove(file)
