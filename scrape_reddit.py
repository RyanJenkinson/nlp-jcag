import pandas as pd
import datetime as dt
from psaw import PushshiftAPI

api = PushshiftAPI()
N = 1000
start_date = int(dt.datetime(2012, 1, 1).timestamp())

res = list(api.search_submissions(after=start_date,
                                  subreddit='Jokes',
                                  filter=['selftext', 'id', 'score', 'title'],
                                  limit=N,
                                  score='>10'))

list_of_dicts = [None] * N
for i in range(N):
    list_of_dicts[i] = res[i].d_

df = pd.DataFrame(list_of_dicts)
df = df[['selftext', 'id', 'score', 'title']]
df.columns = ['body', 'id', 'score', 'title']

df.to_csv('data/scraped_data.csv', encoding='utf-8')