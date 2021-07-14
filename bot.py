import time
import random
import tweepy
from tweepy import api

import os
from dotenv import load_dotenv
import initial_scrape

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET_KEY = os.getenv("API_SECRET_KEY")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET_TOKEN = os.getenv("ACCESS_SECRET_TOKEN")

auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET_TOKEN)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

def follower():
    print("retrieving and following follwers...")
    for follower in tweepy.Cursor(api.followers).items():
        try:
            if not follower.following:
                api.create_friendship(follower.id)
                print(f"{follower.screen_name} was follwed back!")
        except Exception as e:
            pass


def like_retweeter():
    print("retrieving tweets...")
    mentions = tweepy.Cursor(api.mentions_timeline,
                             tweet_mode="extended").items()
    for mention in mentions:
        if mention.user.id == api.me().id:
            return
        if not mention.favorited:
            try:
                mention.favorite()
                print(
                    f"liked {mention.user.screen_name}'s tweet mentioning you")
            except Exception as e:
                pass
        if not mention.retweeted:
            try:
                mention.retweet()
                print(
                    f"retweeted {mention.user.screen_name}'s tweet mentioning you")
            except Exception as e:
                pass


def liker():
    tweets =  tweepy.Cursor(api.user_timeline, id="mi6un_").items()
    for tweet in tweets:
            if not tweet.favorited:
                try:
                    tweet.favorite()
                    print(f"liked {tweet.user.screen_name}'s tweet' ")
                except Exception as e:
                    pass


def post_tweet():
    filename = 'scraped_data/imgs/current.jpg'
    status = open('scraped_data/current_tweet.txt', 'r+')
    api.update_with_media(filename, status.read()+'\n #Art #Artsed #ArtsBlog #Artgallery #Artlovers #Painting #vintage #artist #museumarchive #arts' )

def run():
    while True:
        initial_scrape.art_details()
        post_tweet()
        like_retweeter()
        liker()
        time.sleep(1800)

while __name__ == '__main__':
    run()