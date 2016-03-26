# Nsbe Hacakathon 42
# Beanies
# Youtube Kids App detection
# For educational use for cool people
# Website will be added

from alchemyapi import AlchemyAPI
from flask import render_template
from pymongo import MongoClient
client = MongoClient('mongodb://mitrikyle:Allthatiknow1@ec2-52-11-150-10.us-west-2.compute.amazonaws.com:27017')
db = client.dummyDB
from flask import Flask
from textblob import TextBlob
from DatumBox import DatumBox
import json
import alchemyapi


app = Flask(__name__)

#alchemyapi.apikey = 'de78af95d7e36a826fe4164c7b7fe5763cdbacdf'

# Datum Box API_KEY
API_KEY = "950ac57f58cc94268ac3cf43161c736b"
datum_box = DatumBox(API_KEY)

#for comments in db.nsbeanie_comments.find():
 #    blob = TextBlob( comments['text'])
  #   for sentence in blob.sentences:
   #      print(sentence.sentiment.polarity)
    #     print(sentence.sentiment)
     #    print(sentence.correct())
      #   print(datum_box.twitter_sentiment_analysis(sentence))
       #  print(datum_box.is_adult_content(sentence))

        # print(sentence.sentiment.polarity)
         #print(sentence.sentiment)
         #print(sentence.correct())
         #print(datum_box.twitter_sentiment_analysis(sentence))
         #print(datum_box.is_adult_content(sentence))






@app.route('/')
def hello_world():
    return 'Hello World!'


# route to get all the stats for one channel
@app.route('/get_stats/<channelId>')
def get_stats(channelId):
    comments = db.nsbeanie_comments.find({'channelId': channelId})
    for comment in comments:
        print comment['text'] + " LOL "
    positive = 100
    negative = 1000
    sentiment = {
        "positive": positive,
        "negative": negative
    }

    return render_template('channel_stats.html', sentiment=sentiment)

# route to post one channel to database




if __name__ == '__main__':
    app.debug = True
    app.run()
