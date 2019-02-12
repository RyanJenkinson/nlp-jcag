import csv
import json
from os.path import dirname, join

current_dir = dirname(__file__)
infilename = join(current_dir, "./reddit_jokes.json")
outfilename = join(current_dir, "./jokes_dataset.csv")

infile = open(infilename,'r')
outfile = open(outfilename,'w', encoding='utf-8')

data = json.load(infile)
infile.close()

out = csv.writer(outfile)
out.writerow(data[0].keys())

for row in data:
    try:
        out.writerow(row.values())
        #out.writerow([str(s).encode('utf8') for s in row.values()])
    except UnicodeEncodeError: # Catching errors
        pass