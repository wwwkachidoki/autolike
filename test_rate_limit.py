import tweepy
import os

# 認証
client = tweepy.Client(
    bearer_token=os.environ['BEARER_TOKEN'],
    consumer_key=os.environ['API_KEY'],
    consumer_secret=os.environ['API_SECRET'],
    access_token=os.environ['ACCESS_TOKEN'],
    access_token_secret=os.environ['ACCESS_TOKEN_SECRET']
)

query = "#wagyu"

try:
    # 取得だけ。レスポンスオブジェクトも確認する
    response = client.search_recent_tweets(
        query=query,
        max_results=10,
        tweet_fields=["author_id"]
    )

    if response.data:
        print(f"✅ 正常取得: {len(response.data)}件のツイート")
        for tweet in response.data:
            print(f"- Tweet ID: {tweet.id}, User ID: {tweet.author_id}")
    else:
        print("🔍 ツイートは0件でした（正常）")

except tweepy.TooManyRequests:
    print("❌ レートリミットに達しています。もうしばらく待ってください。")
except Exception as e:
    print(f"❌ その他のエラー: {e}")
