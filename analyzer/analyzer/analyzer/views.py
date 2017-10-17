
from django.shortcuts import render
from .forms import *
import tweepy
from textblob import TextBlob

class app():
	def __init__(self):
		consumer_key = "odSJNTGGkQyxuSw7SPWn0TOoo"
		consumer_secret = "cnX767cXOhHvqN6mj3LYgsczLYmX4iKc1vZ2vwsa0WFLT6nRtI"

		access_token = "1041639684-yplthrA7l3CS0AGcoqlWQ720Lob01UyHdNBNDGS"
		access_secret =  "D17MDBaHsjLLM9pUoNrn2hHslbg52zVCIdWCoXXDAAqCN"
		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token,access_secret)

		self.api = tweepy.API(auth)
		

	def home(self,request):
		self.pos=0
		self.neg=0
		self.neutral=0
		self.tweets=[]
		form = searchForm(request.POST or None)
		context={'form':form}
		if form.is_valid():
			data = form.cleaned_data
			wordToSearch=data['Search']
			public_tweets = self.api.search(wordToSearch,show_user=[True],count=100)

			for tweet in public_tweets:
				# if (not tweet.retweeted) and ('RT @' not in tweet.text):
				print (tweet.user.name + ':' + tweet.text)
				analysis = TextBlob(tweet.text)
				print (analysis.sentiment.polarity)
				polarity_value = analysis.sentiment.polarity
				if polarity_value > 0:
					self.pos+=1
				elif polarity_value < 0:
					self.neg+=1
				else:
					self.neutral+=1
				self.tweets.append(tweet.user.name + ':' + tweet.text)
			print (self.pos,self.neg,self.neutral)
			context={'form':form,'pos':self.pos,'neg':self.neg,'net':self.neutral,'tweets':self.tweets}
		return render(request,"index.html",context)

run=app()