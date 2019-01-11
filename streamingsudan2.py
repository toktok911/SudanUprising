from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler 
from tweepy import API
from tweepy import Cursor
import numpy as np 
import pandas as pd 

import twitter_credentials

class TwitterClient():
	def __init__(self, twitterUser=None):
		self.auth = TwitterAuthenticator().authenticateTwitterApp()
		self.twitterClient = API(self.auth)
		self.twitterUser = twitterUser
	def get_tweets(self, num_tweets):
		tweets = []
		for tweet in Cursor(self.twitterClient.user_timeline, id=self.twitterUser).items(num_tweets):
			tweets.append(tweet)
		return tweets 
	#def getFriendist()
	#def getHomeTimelineTweets()
	def getTwitterClientAPI(self):
		return self.twitterClient
	
class TwitterAuthenticator():
	def authenticateTwitterApp(self):
		auth = OAuthHandler(twitter_credentials.consumer_key, twitter_credentials.consumer_secret)
		auth.set_access_token(twitter_credentials.access_token,twitter_credentials.access_token_secret)
		return auth 

class TwitterStreamer():	
	def __init__(self):
		self.twitterAuthenticator= TwitterAuthenticator()
	def stream_tweets(self, extractedTweets_filename, hashtags_list):
		listener = TwitterListener(extractedTweets_filename)
		auth = self.twitterAuthenticator.authenticateTwitterApp()
		stream = Stream(auth, listener)
		stream.filter(track=hashtags_list)


class TwitterListener(StreamListener):
	def __init__(self,extractedTweets_filename):
		self.extractedTweets_filename = extractedTweets_filename
	def on_data(self,data):
		try:
			print(data)
			with open(self.extractedTweets_filename, 'a') as et:
				et.write(data)
			return True
		except BaseException as e:
			print("Error on data $s" % str(e))
		return True

	def on_error(self, status):
		if status ==420:  # the rate limit thing
			return False # kill the connection
		print(status)

class  TweetsAnalyzer():
	def tweets_to_dataFrame(self, tweets):
		df = pd.DataFrame(data = [tweet.text for tweet in tweets], columns = ['Tweets'])
		#df['id'] = np.array([tweet.id for tweet in tweets])
		#df['device'] = np.array([tweet.source for tweet in tweets])
		df['location'] = np.array([tweet.place for tweet in tweets])
		df['len'] = np.array([len(tweet.text) for tweet in tweets])
		df['likes'] = np.array(tweet.favorite_count for tweet in tweets)
		#df['likes'].astype(int)
		#df['likes'].astype(str).astype(int)

		return df


if __name__ == "__main__":
	twitter_client = TwitterClient()
	twitter_analyzer = TweetsAnalyzer()

	api = twitter_client.getTwitterClientAPI()
	tweets = api.user_timeline(screen_name="toktok911", count=30)
	"""
	for tweet in range(0,30):
		print(tweets[tweet].favorite_count) """

	df = twitter_analyzer.tweets_to_dataFrame(tweets)
	#print(df.dtypes)
	print(np.max(df['likes']))
	#print(df['likes'].max())
	#print(df.head)
	#print('##############################')
	#print(dir(tweets[0]))
	#print('##############################')
	#print(df['likes'])
	#print(df)
	#print(dir(tweets[0]))

	#print(df['len'])
