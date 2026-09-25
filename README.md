# cs4300
In this repository, you will find all my work during the course of Fall 2026, taking CS4300

## Setup

    python3 -m venv homework1_env --system-site-packages
    source homework1_env/bin/activate
    pip install -r Homework_1/requirements.txt

## Running the code

    python3 Homework_1/src/Task1.py

## Running the tests

    cd Homework_1
    pytest -v

## use of ai

    All logic was originally written by me. I plugged in my original code and functionality into pardot which it stated that I did not fulfill
    the requirements. I then used Claude to fix and modify the code so that it is formatted in the correct way for grading. You will also be able
    to see that it is my code by looking at commits: 2899a6c. The changes that ai made was, converting my test scripts to pytest tests, refactor my 
    functions so that it no longer uses the input() command. In Task4, I also had ai remove the explicit type check and added a gitignore and     requirements.txt
