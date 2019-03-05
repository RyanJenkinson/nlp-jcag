import numpy as np
import pandas as pd
import string
import re
from os.path import dirname, join

def clean_dataframe(df,max_wordcount_punchline,max_wordcount_setup, include_removed_jokes = True):
    # Removes special characters from the string
    def string_checker(input_string):
        # Check for no special characters
        if all(char in string.printable for char in input_string):
            return True
        else:
            return False
    
    len_inputdf = len(df)
    print("The size of the input dataframe is: ",len_inputdf)

    # Get indices of rows that dont have any special characters in 
    idx = [string_checker(str(t)) for t in df["title"]] and [string_checker(str(b)) for b in df["body"]]
    df = df[idx]
    print("Removing jokes with title/body containing special characters: ", len(df), "/", len_inputdf)

    # Restrict our attention to those where the title ends in punctuation (should remove spam)
    df = df[df.title.str.contains('[A-Z a-z ?.!"]$', na=False)]
    print("Removing jokes with setups that don't end in [A-Z a-z ?.!\"]: ", len(df), "/", len_inputdf)

    # Make sure the punchline isn't too long
    df = df[df.body.str.split().str.len() <= max_wordcount_punchline]
    df = df[df.title.str.split().str.len() <= max_wordcount_setup]
    print("Restricting the wordcount of the setup and punchline: ", len(df), "/", len_inputdf)

    # Remove any \n or \r tags from the body (sometimes included)
    df['body'] = df['body'].str.replace(r"[\n\r]*", "")

    if not include_removed_jokes:
        df = df[~df.body.isin(['[removed]','[deleted]'])]
        df = df[~df.title.isin(['[removed]','[deleted]'])]

    return df



if __name__ == '__main__':
    current_dir = dirname(__file__)
    infilename = join(current_dir,"../data/raw_data/combined_jokes.zip")

    df = pd.read_csv(infilename)

    cleaned_df = clean_dataframe(df,50,20, include_removed_jokes=True)

    outfilename = join(current_dir,"../data/processed_data/combined_jokes_CLEAN.csv")
    cleaned_df.to_csv(outfilename)