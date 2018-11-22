import tweepy
import time
from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
from random import randint

######For more information on these fields, see this site https://apps.twitter.com/
consumer_key = #Example Consumer Key
consumer_secret = #Consumer Secret Key
access_token = #Access Token Key
access_token_secret = #Access Token Secret Key
######
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

#Sends out example tweets
for k in range(0,10):
    exampleTweet = 'This is an example tweet '+ str(k)
    #update_status updates the account and publishes tweet
    api.update_status(exampleTweet)
    print("just tweeted --> "+ exampleTweet)
    time.sleep(1)
    
