# Nsbe Hacakathon 42
# Beanies
# Youtube Kids App detection
# For educational use for cool people
# Website will be added

from alchemyapi import AlchemyAPI
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

for comments in db.nsbeanie_comments.find():
     blob = TextBlob( comments['text'])
     for sentence in blob.sentences:
         print(sentence.sentiment.polarity)
         print(sentence.sentiment)
         print(sentence.correct())
         print(datum_box.twitter_sentiment_analysis(sentence))
         print(datum_box.is_adult_content(sentence))



#blob = TextBlob(text)
blob.tags           # [('The', 'DT'), ('titular', 'JJ'),
                    #  ('threat', 'NN'), ('of', 'IN'), ...]

blob.noun_phrases   # WordList(['titular threat', 'blob',
                    #            'ultimate movie monster',
                    #            'amoeba-like mass', ...])




#blob.translate(to="es")  # 'La amenaza titular de The Blob...'


@app.route('/')
def hello_world():
    return 'Hello World!'




if __name__ == '__main__':
    app.run()
