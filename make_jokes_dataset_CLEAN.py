import numpy as np
import pandas as pd
import string
import re
from os.path import dirname, join

def clean_dataframe(df,max_wordcount_setup,max_wordcount_punchline):
    """Function to clean the input dataframe according to some rules:
    * Check the string for special characters, only keep those with no special characters in body/title
    * Only keep jokes that end in [?.!"]
    * Restrict to jokes that are have a maximum wordcount in the setup and punchline
    * Removing /n or /r tags from the joke
    
    Arguments:
        df {pandas dataframe} -- Input dataframe to be cleaned
    
    Returns:
        cleaned_df [pandas dataframe] -- Cleaned dataframe
    """

    # Removes special characters from the string
    def string_checker(input_string):
        # Check for no special characters
        if all(char in string.printable for char in input_string):
            return True
        else:
            return False
    # Check the string_checker works and print the size of the dataframe after every cleaning step        
    size_df = len(df)
    print("The length of the input dataframe is: ", len(df))

    # Get indices of rows that dont have any special characters in 
    idx = [string_checker(str(t)) for t in df["title"]] and [string_checker(str(b)) for b in df["body"]]
    df = df[idx]
    print("Removing special characters: ", len(df), "/", size_df)

    # Restrict our attention to those where the title ends in punctuation (should remove spam)
    df = df[df.title.str.contains('[A-Z a-z ?.!"]$')]
    print("Ending in [A-Z a-z ?.!\"]: ", len(df), "/", size_df)

    # Make sure the punchline isn't too long
    df = df[df.body.str.split().str.len() <= max_wordcount_punchline]
    df = df[df.title.str.split().str.len() <= max_wordcount_setup]
    print("Restricting wordcounts on punchline and setup: ", len(df), "/", size_df)

    # Remove any \n or \r tags from the body (sometimes included)
    df['body'] = df['body'].str.replace(r"[\n\r]*", "")

    return df


if __name__ == '__main__':
    # Get the dataframe we want to clean
    current_dir = dirname(__file__)
    infilename = join(current_dir,"./jokes_dataset.csv")
    df = pd.read_csv(infilename)

    # Clean the dataframe
    cleaned_df = clean_dataframe(df,50,20)

    # Save the cleaned dataframe
    outfilename = join(current_dir,"./jokes_dataset_CLEAN.csv")
    cleaned_df.to_csv(outfilename)