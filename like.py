import tweepy
import os
import time

# 認証
client = tweepy.Client(
    bearer_token=os.environ['BEARER_TOKEN'],
    consumer_key=os.environ['API_KEY'],
    consumer_secret=os.environ['API_SECRET'],
    access_token=os.environ['ACCESS_TOKEN'],
    access_token_secret=os.environ['ACCESS_TOKEN_SECRET']
)

# 検索条件
query = "#wagyu OR #halalburger"

# ツイート検索（7件だけ）
try:
    tweets = client.search_recent_tweets(query=query, max_results=7, tweet_fields=["author_id"]).data
except tweepy.TooManyRequests:
    print("Rate limit reached. Try again later.")
    exit()
except Exception as e:
    print(f"Search error: {e}")
    exit()

# 自動いいね＋フォロー処理
if tweets:
    for tweet in tweets:
        try:
            # いいね
            client.like(tweet.id)
            print(f"Liked tweet: {tweet.id}")

            # フォロー（同じ作者を繰り返しフォローしないよう注意）
            client.follow_user(tweet.author_id)
            print(f"Followed user: {tweet.author_id}")

            time.sleep(5)  # 間隔調整（スパム防止）

        except tweepy.TooManyRequests:
            print("Rate limit hit. Stopping.")
            break
        except Exception as e:
            print(f"Error: {e}")
