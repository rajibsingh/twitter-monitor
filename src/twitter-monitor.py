import twitter
from pymongo import MongoClient
from textblob import TextBlob
import configparser
from textstat.textstat import textstat
import json
import os

config = configparser.ConfigParser()
print("current directory {0}".format(os.getcwd()))
config.read("../config.ini")

api = twitter.Api(consumer_key=config['global']['consumer_key'],
                      consumer_secret=config['global']['consumer_secret'],
                      access_token_key=config['global']['access_token_key'],
                      access_token_secret=config['global']['access_token_secret'])

client = MongoClient()
tweets_coll = client.contentdb.tweet
author_coll = client.contentdb.author

def downloadTweets(statuses):
    for x in statuses:
        jsontweet = x.AsDict()
        id = jsontweet["id"]
        jsontweet['_id'] = jsontweet["id"]
        tweets_coll.update_one({'id':id}, {'$set' : jsontweet}, upsert=True)

def getAuthors():
    return(list(author_coll.find({}, {"username": 1, "_id": 0})))

authors = getAuthors()
for author in authors:
    author = author["username"]
    tweets = api.GetUserTimeline(screen_name=author)
    downloadTweets(tweets)

# Analyzing Tweets
processed_tweets_coll = client.contentdb.processed_tweets

def analyzeTweet(tweetId):
    tweet = tweets_coll.find_one({"_id":tweetId})
    print("tweet: ", tweet)
    tweetAnalysis = {"_id":tweet["id"]}
    print("\tanalyzed tweet:", tweetAnalysis)
    blob = TextBlob(tweet["text"])
    tweetAnalysis["tags"] = blob.tags
    tweetAnalysis["noun_phrases"] = blob.noun_phrases
    tweetAnalysis["sentiment.polarity"] = blob.sentiment[0]
    tweetAnalysis["sentiment.subjectivity"] = blob.sentiment[1]
    tweetAnalysis["flesch_kincaid"] = textstat.flesch_kincaid_grade(tweet["text"])
    tweetAnalysis["average_sentence_length"] = textstat.avg_sentence_length(tweet["text"])
    tweetAnalysis["average_syllables_per_word"] = textstat.avg_syllables_per_word(tweet["text"])
    print("\ttweetAnalyis: " + json.dumps(tweetAnalysis))
    processed_tweets_coll.update_one({"_id":tweet["id"]}, {'$set' : tweetAnalysis}, upsert=True)

def processTweets():
    received_tweets = list(tweets_coll.find({},{"_id":1}))
    received_tweets = set(map((lambda dict_id: dict_id["_id"]), received_tweets))

    processed_tweets = list(processed_tweets_coll.find({},{"_id":1}))
    processed_tweets = set(map((lambda dict_id: dict_id["_id"]), processed_tweets))

    print("we have these tweets in the db:", received_tweets)
    print("we have the following tweets in processed_tweets", processed_tweets)
    unprocessed_tweets = received_tweets - processed_tweets
    print("the tweets to be processed are: ", unprocessed_tweets)
    for tweet in unprocessed_tweets:
        analyzeTweet(tweet)

processTweets()








