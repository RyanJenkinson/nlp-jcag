import numpy as np
import pandas as pd
import string
import re
from os.path import dirname, join

current_dir = dirname(__file__)
filename = join(current_dir,"./jokes_dataset_CLEAN.csv")

df = pd.read_csv(filename)

print(df.iloc[522,:]['body'])
print(df.iloc[523,:]['body'])