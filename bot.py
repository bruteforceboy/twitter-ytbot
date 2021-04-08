#author: bruteforceboy

import tweepy
import geocoder
import time
import random
import os
from os import environ

CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']

ACCESS_KEY = environ['ACCESS_KEY']
ACCESS_SECRET = environ['ACCESS_SECRET']

auth = tweepy.OAuthHandler(CONSUMER_KEY, 
    CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, 
    ACCESS_SECRET)

api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")

# timeline = api.home_timeline()
# for tweet in timeline:
# 	print(f"{tweet.user.name} said {tweet.text}")

# api.update_status("tweet from twitter bot!")

g = geocoder.osm('Nigeria')
closest_loc = api.trends_closest(g.lat, g.lng)
trends_result = api.trends_place(closest_loc[0]['woeid'])
trends = set([trend['name'] for trend in trends_result[0]['trends']])

lines = ["If you want a laugh then this video is for you ",\
			"Check out my video ", "Yo! check this video out "]

yt_video = "https://www.youtube.com/watch?v=wvoBLb6QkKI\n"

count = 0

while True: 
	if count % 6 == 0: 
		# 30 minutes (like for follow)
		search = ('#ifb OR #likeforfollow OR #followtrain')
		nmTweets = 30

		for tweet in tweepy.Cursor(api.search, search, lang='en').items(nmTweets):
			# print(f"{tweet.user.name} said {tweet.text}")
			if not tweet.favorited:
				try:
					tweet.favorite()
					#tweet.retweet()
					time.sleep(5)
				except: 
					print("error while liking")
		#For Followback to the Followers            	
		for follower in tweepy.Cursor(api.followers).items(1):
			if not follower.following:
				if follower.friends_count > 50:
					follower.follow()

	orig = lines[random.randint(0, len(lines) - 1)] + yt_video
	tweet = orig
	for trend in trends: 
		new_tweet = tweet + trend + " "
		if len(new_tweet) > 186: 
			api.update_status(tweet)
			tweet = orig + trend + " "
		else: 
			tweet = new_tweet

	if len(tweet) > 0:
		api.update_status(tweet)
	print("proc " + str(count) + " was successful!")
	count += 1
	time.sleep(300)