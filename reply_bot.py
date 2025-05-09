import tweepy
import openai
import os
from dotenv import load_dotenv

load_dotenv()  # .envがある場合は使えるようにする

# Twitter 認証
client = tweepy.Client(
    bearer_token=os.environ["BEARER_TOKEN"],
    consumer_key=os.environ["API_KEY"],
    consumer_secret=os.environ["API_SECRET"],
    access_token=os.environ["ACCESS_TOKEN"],
    access_token_secret=os.environ["ACCESS_TOKEN_SECRET"]
)

# OpenAI API 認証
openai.api_key = os.environ["OPENAI_API_KEY"]

# 自分のユーザー名（@なし）
username = os.environ["MY_USERNAME"]

# 自分宛ての最新メンション（リプライ）を取得
query = f"to:{username} -is:retweet"
tweets = client.search_recent_tweets(query=query, max_results=10, tweet_fields=["author_id"]).data

if tweets:
    for tweet in tweets:
        try:
            prompt = f"お客様からの質問に、丁寧で自然な敬語で返信してください：{tweet.text}"
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            reply_text = response.choices[0].message.content.strip()

            # ユーザーID（@ではなく数値）からユーザー名を取得
            user = client.get_user(id=tweet.author_id).data
            reply = f"@{user.username} {reply_text}"

            # リプライ投稿
            client.create_tweet(in_reply_to_tweet_id=tweet.id, text=reply)
            print(f"✅ Replied to tweet: {tweet.id}")

        except Exception as e:
            print(f"❌ Error: {e}")
else:
    print("🔍 No recent mentions found.")
