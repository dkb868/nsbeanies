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

for comments in db.nsbeanie_comments.find():
     comment_id = comments['_id']
     blob = TextBlob( comments['text'])
     for sentence in blob.sentences:
         print(sentence.sentiment.polarity)
         print(sentence.sentiment)
         print(sentence.correct())
         print(datum_box.twitter_sentiment_analysis(sentence))
         print(datum_box.is_adult_content(sentence))

         polarity = str(sentence.sentiment.polarity)
         sentiment = str(sentence.sentiment)
         correct = str(sentence.correct())
         twitter = str(datum_box.twitter_sentiment_analysis(sentence))
         adult= str(datum_box.is_adult_content(sentence))
         response = alchemyapi2.language('text', blob)

         if response['status'] == 'OK':
            print('## Response Object ##')
            print(json.dumps(response, indent=4))
            language_response = (json.dumps(response, indent=4))



         if response['status'] == 'OK':
            print('## Response Object ##')
            categories_response = (json.dumps(response, indent=4))



         if response['status'] == 'OK':
            print('## Response Object ##')
            print(json.dumps(response, indent=4))
            targetSentiment = (json.dumps(response, indent=4))

# route to post one channel to database



         if response['status'] == 'OK':
            print('## Response Object ##')
            print(json.dumps(response, indent=4))
            keywords_response = (json.dumps(response, indent=4))

            print('')
            print('## Keywords ##')
            for keyword in response['keywords']:
                print('text: ', keyword['text'].encode('utf-8'))
                print('relevance: ', keyword['relevance'])
                print('sentiment: ', keyword['sentiment']['type'])
                if 'score' in keyword['sentiment']:
                    print('sentiment score: ' + keyword['sentiment']['score'])
                print('')
         else:
            print('Error in keyword extaction call: ', response['statusInfo'])

         # save sentiment
         sentiment = {
             'polarity' : polarity,
             'sentiment' : sentiment,
             'correct' : correct,
             'twitter' : twitter,
             'adult' : adult,
        #     'language_response' :language_response,
      #       'categories_response' : categories_response,
      #       'targetSentiment' : targetSentiment,
      #       'keywords_response' : keywords_response
         }
         db.nsbeanie_sentiments.insert_one(sentiment)
         print "succesfully inserted"




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




if __name__ == '__main__':
    app.debug = True
    app.run()
