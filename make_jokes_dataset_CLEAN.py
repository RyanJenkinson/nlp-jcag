import numpy as np
import pandas as pd
import string
import re
from os.path import dirname, join

current_dir = dirname(__file__)
filename = join(current_dir,"./jokes_dataset.csv")

df = pd.read_csv(filename)

# Removes special characters from the string
def string_checker(input_string):
    # Check for no special characters
    if all(char in string.printable for char in input_string):
        return True
    else:
        return False
print(string_checker("It's Ryan"))
print(len(df))
# Get indices of rows that dont have any special characters in 
idx = [string_checker(str(t)) for t in df["title"]] and [string_checker(str(b)) for b in df["body"]]
df = df[idx]
print(len(df))
# Restrict our attention to those where the title ends in punctuation (should remove spam)
df = df[df.title.str.contains('[?.!]$')]
print(len(df))
# Make sure the punchline isn't too long
punchline_wordcount = 20
df = df[df.body.str.split().str.len() <= 20]
print(len(df))

# Remove any \n or \r tags from the body (sometimes included)
df['body'] = df['body'].str.replace(r"[\n\r]*", "")

outfilename = join(current_dir,"./jokes_dataset_CLEAN.csv")
df.to_csv(outfilename)