import numpy as np
import pandas as pd
import time
import datetime as dt
from psaw import PushshiftAPI

api = PushshiftAPI()
# As of now, 1000 is the maximum limit for scraping using this API.
scrape_limit = 1000

# Create a blank dataframe which we push to a csv to store our data
df_all = pd.DataFrame(columns=['datetime','body', 'id', 'score', 'title'])
df_all.to_csv('data/scraped_data_score10+.csv', encoding='utf-8')

# Loop over (day,month,year) in a given range
loop_start_date = dt.datetime(2009, 1,1)
loop_end_date = dt.datetime(2019, 1,1)
loop_step = dt.timedelta(days = 1)
dates = np.arange(loop_start_date, loop_end_date, loop_step).astype(dt.datetime)

for date in dates:
    day, month, year = date.day, date.month, date.year
    start_date = int(dt.datetime(year, month, day).timestamp())

    res = list(api.search_submissions(after=start_date,
                                    subreddit='Jokes',
                                    filter=['selftext', 'id', 'score', 'title'],
                                    limit=scrape_limit,
                                    score='>10',
                                    sort='asc'))

    list_of_dicts = []
    list_empty = True
    for i in range(scrape_limit):
        # Check that the id is unique i.e not already in the dataframe. If it is, append it
        if not any(df_all['id'].str.contains(res[i].d_['id'])):
            list_empty = False
            list_of_dicts.append(res[i].d_)

    if not list_empty:
        df = pd.DataFrame(list_of_dicts)
        df = df[['selftext', 'id', 'score', 'title']]
        df.columns = ['body', 'id', 'score', 'title'] # Rename the columns

        # Insert the datetime tag, this will allow us to resume scraping from where we left off if it crashes
        df.insert(loc=0, column='datetime', value='_'.join([str(day),str(month),str(year)]))
        # Insert a time.sleep(1) just in case we overrun the API
        time.sleep(1)
        # Append df_all and save to csv in case it crashes
        df_all = pd.concat([df_all,df])
        df.to_csv('data/scraped_data_score10+.csv', encoding='utf-8', mode = 'a', header=False)