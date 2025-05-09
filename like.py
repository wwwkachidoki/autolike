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

# ✅ Secretsからアカウント名を取得
username = os.environ['TWITTER_USERNAME']

# 自分のユーザーIDを取得
try:
    my_user = client.get_user(username="wagyu_worldwide")
    my_user_id = my_user.data.id
except Exception as e:
    print(f"Failed to get user ID: {e}")
    exit()

# ====== STEP 1: いいね＋フォロー ======
query = "#wagyu OR #halalburger"

try:
    tweets = client.search_recent_tweets(query=query, max_results=7, tweet_fields=["author_id"]).data
except tweepy.TooManyRequests:
    print("Rate limit reached. Try again later.")
    exit()
except Exception as e:
    print(f"Search error: {e}")
    exit()

if tweets:
    for tweet in tweets:
        try:
            client.like(tweet.id)
            print(f"Liked tweet: {tweet.id}")

            client.follow_user(tweet.author_id)
            print(f"Followed user: {tweet.author_id}")

            time.sleep(5)
        except tweepy.TooManyRequests:
            print("Rate limit hit during like/follow. Stopping.")
            break
        except Exception as e:
            print(f"Like/Follow error: {e}")

# ====== STEP 2: アンフォロー（500人超過時のみ、最大30件） ======
try:
    following_response = client.get_users_following(id=my_user_id, max_results=1000)
    following_list = following_response.data if following_response and following_response.data else []

    if len(following_list) > 500:
        print(f"Currently following {len(following_list)} users. Starting unfollow process...")

        count = 0
        for user in following_list:
            try:
                client.unfollow_user(user.id)
                print(f"Unfollowed user: {user.username}")
                count += 1
                time.sleep(3)
                if count >= 30:
                    print("Unfollowed max 30 users.")
                    break
            except Exception as e:
                print(f"Unfollow error: {e}")
except Exception as e:
    print(f"Error fetching following list: {e}")
