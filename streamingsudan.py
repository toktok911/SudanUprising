from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler 

import twitter_credentials1

class TwitterStreamer():	

	def __init__(self):
		pass

	def stream_tweets(self, extractedTweets_filename, hashtags_list):
		listener = StdOutListener(extractedTweets_filename)
		auth = OAuthHandler(twitter_credentials.consumer_key, twitter_credentials.consumer_secret)
		auth.set_access_token(twitter_credentials.access_token,twitter_credentials.access_token_secret)
		stream = Stream(auth, listener)
		stream.filter(track=hashtags_list)


class StdOutListener(StreamListener):
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
		print(status)

if __name__ == "__main__":
	hashtags_list = ['SudanUprising', 'SudanRevolts', 'مدن_السودان_تنتفض','تسقط_بس']
	extractedTweets_filename = "tweets.json"
	twitterStreamer = TwitterStreamer()
	twitterStreamer.stream_tweets(extractedTweets_filename,hashtags_list)
