import sys
import pandas as pd

def create_corpus(corpus_folder, df):
    for index, row in df.iterrows():
        text = str(row['title']) + ' ' + str(row['body'])
        fname = str(index) + '.txt'
        corpus_file = open(corpus_folder + '/' + fname, 'a', encoding='utf-8')
        corpus_file.write(str(text))
        corpus_file.close()

corpus_folder = sys.argv[1]
df = pd.read_csv(sys.argv[2])

create_corpus(corpus_folder, df)