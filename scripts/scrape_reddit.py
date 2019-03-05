import numpy as np
import pandas as pd
import json
import time
import datetime as dt
from psaw import PushshiftAPI
from os.path import dirname, join

api = PushshiftAPI()
# As of now, 1000 is the maximum limit for scraping using this API.
scrape_limit = 1000

# Save output file name
current_dir = dirname(__file__)
outfilename = join(current_dir,'../data/processed_data/scraped_data_v4.csv')

# Create a blank dataframe which we push to a csv to store our data
df_all = pd.DataFrame(columns=['datetime','body', 'id', 'score', 'title'])
df_all.to_csv(outfilename, encoding='utf-8')

# Loop over (day,month,year) in a given range
loop_start_date = dt.datetime(2017, 5,1)
loop_end_date = dt.datetime(2019, 1,1)
loop_step = dt.timedelta(days = 1)
dates = np.arange(loop_start_date, loop_end_date, loop_step).astype(dt.datetime)

for count,date in enumerate(dates):
    # Get day, month, year and instantiate a starting date for scraping
    day, month, year = date.day, date.month, date.year
    start_date = int(dt.datetime(year, month, day).timestamp())

    # Since our API returns many duplicates, periodically purge the df and de-duplicate
    if (count > 0) and (count % 100 == 0):
        df_all = df_all.drop_duplicates('id')
        print("Up to, but not including, date " + str(dt.date(year, month, day)),
         "(" + str(count) + " days scraped), there are " + str(len(df_all)) + " unique jokes in the dataset.")
        df_all.to_csv(outfilename, encoding='utf-8')

        # UNCOMMENT THE BELOW TO INSTEAD SAVE AS JSON 
        # with open(outfilename, 'w') as f:
        #     json.dump(df_all.to_dict(orient='records'), f)

    for score_threshold in ['<10','>10','>50','>100']:
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

        # Append df_all and save in case it crashes
        df_all = pd.concat([df_all,df])

# When we have finished the loop, de-duplicate again
df_all = df_all.drop_duplicates('id')
# Check for any duplications of title and body but for different ids
df_all = df_all.drop_duplicates(['title','body'])

# Overwrite the csv file with final dataframe
df_all.to_csv(outfilename, encoding='utf-8')