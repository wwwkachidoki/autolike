import tweepy
import os
import time

client = tweepy.Client(
    bearer_token=os.environ['BEARER_TOKEN'],
    consumer_key=os.environ['API_KEY'],
    consumer_secret=os.environ['API_SECRET'],
    access_token=os.environ['ACCESS_TOKEN'],
    access_token_secret=os.environ['ACCESS_TOKEN_SECRET']
)

query = "#wagyu OR #halalburger"

try:
    tweets = client.search_recent_tweets(query=query, max_results=10).data
except Exception as e:
    print(f"Search error: {e}")
    exit()

if tweets:
    for tweet in tweets:
        try:
            client.like(tweet.id)
            print(f"Liked tweet: {tweet.id}")
            time.sleep(5)
        except tweepy.TooManyRequests:
            print("Rate limit hit. Stopping.")
            break
        except Exception as e:
            print(f"Error: {e}")
