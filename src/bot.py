import time
import random
import tweepy
from tweepy import api

import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET_KEY = os.getenv("API_SECRET_KEY")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET_TOKEN = os.getenv("ACCESS_SECRET_TOKEN")

auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET_TOKEN)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

art_accounts = ["mia_japankorea", "cezanneart", "SovietArtBot", "aic_african"]


def retweeter():
    while True :
        userId = random.choice(art_accounts)
        for tweet in tweepy.Cursor(api.user_timeline, id = userId).items():
            try:
                if not tweet.retweeted:
                    tweet.retweet()
                    print(f"Retweeted {userId}'s tweet")
                    time.sleep(5)
                    break

                   

            except Exception as e:
                print("Error!", e)
                pass


def follower():
    print("retrieving and following follwers...")
    for follower in tweepy.Cursor(api.followers).items():
        try:
            if not follower.following:
                api.create_friendship(follower.id)
                print(f"{follower.screen_name} was follwed back!")
        except Exception as e:
            print("error occured", e)
            pass


def like_retweeter():
    print("retrieving tweets...")
    mentions = tweepy.Cursor(api.mentions_timeline, tweet_mode="extended").items()
    for mention in mentions:
        if mention.user.id == api.me().id:
            return
        if not mention.favorited:
            try:
                mention.favorite()
                print(f"liked {mention.user.screen_name}'s tweet mentioning you")
            except Exception as e:
                print("error!", e)
                pass
        if not mention.retweeted:
            try:
                mention.retweet()
                print(f"retweeted {mention.user.screen_name}'s tweet mentioning you")
            except Exception as e:
                print("error!", e)
                pass


follower()
like_retweeter()
retweeter()
