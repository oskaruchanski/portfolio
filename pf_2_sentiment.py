# sentiment analysis of Tweets
import pandas as pd
import tweepy
from textblob import TextBlob

# set keys
consumer_key = 'YOUR_CODE_HERE'
consumer_secret = 'YOUR_CODE_HERE
access_token = 'YOUR_CODE_HERE'
access_token_secret = 'YOUR_CODE_HERE'

# handle authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# set main variable
api = tweepy.API(auth)

# search for your keyword
public_tweets = api.search('trump', lang='en', count=100)

# harverst data
tweets = {}
for i, tweet in enumerate(public_tweets):
    tweets[i] = {'id': tweet._json['id'],
                 'date': tweet._json['created_at'],
                 'user': tweet._json['user']['name'],
                 'text': tweet._json['text'],
                 'favour': tweet._json['favorite_count'],
                 'retweet': tweet._json['retweet_count'],
                 'polarity': TextBlob(tweet._json['text']).sentiment.polarity,
                 'subjectivity': TextBlob(tweet._json['text']).sentiment.subjectivity, }

# set db variable
tweets_db = pd.DataFrame.from_dict(tweets, orient='index')
tweets_db.to_csv('tweets.csv')
