import tweepy
import openai
import os
import time
from dotenv import load_dotenv

# .envファイルの読み込み（ローカルテスト用）
load_dotenv()

# Twitter 認証
client = tweepy.Client(
    bearer_token=os.environ["BEARER_TOKEN"],
    consumer_key=os.environ["API_KEY"],
    consumer_secret=os.environ["API_SECRET"],
    access_token=os.environ["ACCESS_TOKEN"],
    access_token_secret=os.environ["ACCESS_TOKEN_SECRET"]
)

# OpenAI 認証
openai.api_key = os.environ["OPENAI_API_KEY"]

# ユーザー名の取得
username = os.environ.get("MY_USERNAME")
if not username:
    raise ValueError("❌ 環境変数 'MY_USERNAME' が設定されていません。")

# クエリ作成（自分宛のメンション、リツイート除外）
query = f'to:{username} -is:retweet'
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

# ツイートがあれば処理開始
if tweets:
    for tweet in tweets:
        try:
            prompt = f"お客様からの質問に、丁寧で自然な敬語で返信してください：{tweet.text}"
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            reply_text = response.choices[0].message.content.strip()

            user = client.get_user(id=tweet.author_id).data
            reply = f"@{user.username} {reply_text}"

            client.create_tweet(in_reply_to_tweet_id=tweet.id, text=reply)
            print(f"✅ Replied to tweet: {tweet.id}")

            time.sleep(20)  # レート制限対策（1ツイートごとに5秒待機）

        except Exception as e:
            print(f"❌ リプライエラー: {e}")
else:
    print("🔍 リプライ対象のメンションは見つかりませんでした。")
