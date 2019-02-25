import praw
import pandas as pd
import datetime as dt

# TO DO: Remove info when we make our GitHub Public
reddit = praw.Reddit(client_id='GODFmBxq92To5Q', \
                     client_secret='ZvhZ6sueZyArNUTjkru1nfDUgk8', \
                     user_agent='joke_scrapr', \
                     username='joke_scrapr', \
                     password='Russellr93')

subreddit = reddit.subreddit('Jokes')

top_subreddit = subreddit.top(limit=1000)

joke_dict = { "body":[],
              "id":[],
              "score":[],
              "title":[]}

for submission in top_subreddit:
    joke_dict["body"].append(submission.selftext)
    joke_dict["id"].append(submission.id)
    joke_dict["score"].append(submission.score)
    joke_dict["title"].append(submission.title)

joke_data = pd.DataFrame(joke_dict)

joke_data.to_csv('data/scraped_jokes.csv')