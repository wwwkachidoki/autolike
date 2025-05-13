import os
import tweepy
import openai
from openai import OpenAI
from dotenv import load_dotenv

# .env 読み込み（ローカル実行時）
load_dotenv()

# Twitter 認証
client = tweepy.Client(
    bearer_token=os.environ["BEARER_TOKEN"],
    consumer_key=os.environ["API_KEY"],
    consumer_secret=os.environ["API_SECRET"],
    access_token=os.environ["ACCESS_TOKEN"],
    access_token_secret=os.environ["ACCESS_TOKEN_SECRET"]
)

# OpenAI 認証（新バージョン対応）
openai_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# ユーザー名の取得（@なし）
username = os.environ.get("TWITTER_USERNAME")
if not username:
    raise ValueError("❌ 環境変数 'TWITTER_USERNAME' が設定されていません。")

query = f'to:{username} -is:"retweet"'
print(f"🟡 Query: {query}")

try:
    tweets = client.search_recent_tweets(
        query=query,
        max_results=10,
        tweet_fields=["author_id"]
    ).data
except Exception as e:
    print(f"❌ 検索エラー: {e}")
    exit()

if tweets:
    for tweet in tweets:
        try:
            prompt = f"お客様からの質問に、丁寧で自然な敬語で返信してください：{tweet.text}"
            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            reply_text = response.choices[0].message.content.strip()

            user = client.get_user(id=tweet.author_id).data
            reply = f"@{user.username} {reply_text}"
            client.create_tweet(in_reply_to_tweet_id=tweet.id, text=reply)
            print(f"✅ Replied to tweet: {tweet.id}")

        except Exception as e:
            print(f"❌ リプライエラー: {e}")
else:
    print("🔍 リプライ対象のメンションは見つかりませんでした。")
