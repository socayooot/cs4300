"""
This task instructs me to take in a file as input and then count the amount 
of words in it 
"""

def count_words_in_file(file_path):
    """
    Return the number of words in the given text file.

    :raises FileNotFoundError: if file_path does not exist.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        contents = f.read()

    count = len(contents.split())
    return count