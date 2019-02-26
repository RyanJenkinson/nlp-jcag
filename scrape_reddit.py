import pandas as pd
import time
import datetime as dt
from psaw import PushshiftAPI

api = PushshiftAPI()
# As of now, 1000 is the maximum limit for scraping using this API.
scrape_limit = 1000

# Create a blank dataframe which we push to a csv to store our data
df = pd.DataFrame(columns=['body', 'id', 'score', 'title'])
df.to_csv('data/scraped_data.csv', encoding='utf-8')

# Loop over (day,month,year) in a given range
for year in range(2012,2019):
    for month in range(1, 13):
        for day in range(1,29):
            start_date = int(dt.datetime(year, month, day).timestamp())

            res = list(api.search_submissions(after=start_date,
                                            subreddit='Jokes',
                                            filter=['selftext', 'id', 'score', 'title'],
                                            limit=scrape_limit,
                                            score='>10',
                                            sort='asc'))

            list_of_dicts = [None] * scrape_limit
            for i in range(scrape_limit):
                list_of_dicts[i] = res[i].d_

            df = pd.DataFrame(list_of_dicts)
            df = df[['selftext', 'id', 'score', 'title']]
            df.columns = ['body', 'id', 'score', 'title']
            time.sleep(5)
            # Append the csv
            df.to_csv('data/scraped_data.csv', encoding='utf-8', mode = 'a', header=False)