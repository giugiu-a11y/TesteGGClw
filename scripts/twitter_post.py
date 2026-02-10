#!/usr/bin/env python3
import tweepy
import os
import sys

# Credentials
consumer_key = os.environ.get('TWITTER_CONSUMER_KEY')
consumer_secret = os.environ.get('TWITTER_CONSUMER_SECRET')
access_token = os.environ.get('TWITTER_ACCESS_TOKEN')
access_token_secret = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')

# Auth with v2
client = tweepy.Client(
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
)

# Get tweet text from argument
if len(sys.argv) > 1:
    tweet_text = ' '.join(sys.argv[1:])
else:
    tweet_text = sys.stdin.read().strip()

# Post
try:
    response = client.create_tweet(text=tweet_text)
    print(f"✅ Tweet posted! ID: {response.data['id']}")
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
