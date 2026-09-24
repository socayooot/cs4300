"""
This task instructs me to take in a file as input and then count the amount 
of words in it 
"""

def count_words_in_file(file):
        with open(file, "r", encoding="utf-8") as f:
            contents = f.read()

        count = len(contents.split())
        return(count)