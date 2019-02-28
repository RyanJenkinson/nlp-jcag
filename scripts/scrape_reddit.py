import numpy as np
import pandas as pd
import time
import datetime as dt
from psaw import PushshiftAPI

api = PushshiftAPI()
# As of now, 1000 is the maximum limit for scraping using this API.
scrape_limit = 1000
# Save output file name
outfilename = '../data/processed_data/scraped_data.csv'
# Create a blank dataframe which we push to a csv to store our data
df_all = pd.DataFrame(columns=['datetime','body', 'id', 'score', 'title'])
df_all.to_csv(outfilename, encoding='utf-8')

# Loop over (day,month,year) in a given range
loop_start_date = dt.datetime(2009, 1,1)
loop_end_date = dt.datetime(2019, 1,1)
loop_step = dt.timedelta(days = 1)
dates = np.arange(loop_start_date, loop_end_date, loop_step).astype(dt.datetime)

for count,date in enumerate(dates):
    # Since our API returns many duplicates, periodically purge the df and de-dup
    if (count > 0) and (count % 100 == 0):
        df_all = df_all.drop_duplicates('id')

    for score_threshold in ['<10','>10','>50','>100']:
        day, month, year = date.day, date.month, date.year
        start_date = int(dt.datetime(year, month, day).timestamp())

        res = list(api.search_submissions(after=start_date,
                                        subreddit='Jokes',
                                        filter=['selftext', 'id', 'score', 'title'],
                                        limit=scrape_limit,
                                        score=score_threshold,
                                        sort='asc'))

        list_of_dicts = [None] * scrape_limit
        for i in range(scrape_limit):
            list_of_dicts[i] = res[i].d_

        df = pd.DataFrame(list_of_dicts)
        df = df[['selftext', 'id', 'score', 'title']]
        df.columns = ['body', 'id', 'score', 'title'] # Rename the columns

        # Insert the datetime tag, this will allow us to resume scraping from where we left off if it crashes
        df.insert(loc=0, column='datetime', value='_'.join([str(day),str(month),str(year)]))

        # Append df_all and save to csv in case it crashes
        df_all = pd.concat([df_all,df])
        df.to_csv(outfilename, encoding='utf-8', mode = 'a', header=False)

# When we have finished the loop, de-duplicate again
df_all = df_all.drop_duplicates('id')
# Check for any duplications of title and body but for different ids
df_all = df_all.drop_duplicates(['title','body'])