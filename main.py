from sqlalchemy import values
from textblob import TextBlob
import tweepy
import sys
import config
import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import os
import nltk
import re
import string
from wordcloud import WordCloud, STOPWORDS
from IPython.display import display
from PIL import Image
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem import SnowballStemmer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer

with open("config.json", "r") as jsonfile:
    data = json.load(jsonfile)
    # print("Read successful")
# print(data)

api_key=(data['api_key'])
api_key_secret=(data['api_key_secret'])
access_token=(data['access_token'])
access_token_secret=(data['access_token_secret'])

auth_handler = tweepy.OAuthHandler(consumer_key=api_key,consumer_secret=api_key_secret)
auth_handler.set_access_token(access_token,access_token_secret)
api = tweepy.API(auth_handler)

search_term = input("Please enter the term to search: ")
# search_term = 'AI'

tweet_amount  = int(input("Please enter the number of tweets to search: "))
# tweet_amount = 300

polarity = 0
positive = 0
neutral = 0
negative = 0

tweets = tweepy.Cursor(api.search_tweets, q=search_term, lang='en').items(tweet_amount)

for tweet in tweets:
    final_text = tweet.text.replace('RT','')
    if final_text.startswith(' @'):
      position = final_text.index(':')
      final_text = final_text[position+2:]
    if final_text.startswith('@'):
      position = final_text.index(' ')
      final_text = final_text[position+2:]
    # print(final_text)
    analysis = TextBlob(final_text)
    tweet_polarity = analysis.polarity
    if tweet_polarity > 0.00:
        positive += 1
    elif tweet_polarity < 0.00:
        negative += 1
    elif tweet_polarity == 0.00:
        neutral += 1 
    # print(analysis.sentiment)
    polarity += tweet_polarity

print("Polarity:" , polarity)
print(f'Amount of Positive Tweets: {positive}')
print(f'Amount of Negative Tweets: {negative}')
print(f'Amount of Neutral Tweets: {neutral}')

x = positive
y = negative
z = neutral

graph = np.array([x,y,z])
plt.pie(graph, labels=['Positive', 'Negative', 'Neutral'],explode=[0.075,0.075,0.075])
plt.title("Sentiment Analysis of Keyword: "+search_term+"")
plt.legend()
plt.show()

# #Function to Create Wordcloud
# def create_wordcloud(text):
#     mask = np.array(Image.open("cloud.png"))
#     stopwords = set(STOPWORDS)
#     wc = WordCloud(background_color="white",
#     mask = mask,
#     max_words=3000,
#     stopwords=stopwords,
#     repeat=True)
#     wc.generate(str(text))
#     wc.to_file("wc.png")
#     print("Word Cloud Saved Successfully")
#     path="wc.png"
#     display(Image.open(path))

# create_wordcloud(int(search_term["text"]).values)