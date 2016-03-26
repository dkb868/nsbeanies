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



app = Flask(__name__)
# Datum Box API_KEY
API_KEY = "950ac57f58cc94268ac3cf43161c736b"
datum_box = DatumBox(API_KEY)
alchemyapi2 = AlchemyAPI()




import smtplib
# Here are the email package modules we'll need
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
msg = MIMEMultipart()
userAddress ="postmaster@sandboxf32a8e5d26ea4769a1e20168754971a5.mailgun.org"
userPassword ="8e14d70dd060c158212a4f7b438f7b79"
server = smtplib.SMTP('smtp.mailgun.org', 587)
server.starttls()
server.login(userAddress, userPassword)

msg = "YOUR MESSAGE!"
html = """\
<html>
  <head></head>
  <body>
    <p>Hi!<br>
       How are you?<br>
       Here is the <a href="http://www.python.org">link</a> you wanted.
    </p>
  </body>
</html>
"""
server.sendmail(userAddress,"krystal.folkes@gmail.com", msg)
server.quit()

for comments in db.nsbeanie_comments.find():
     blob = TextBlob( comments['text'])
     for sentence in blob.sentences:
         print(sentence.sentiment.polarity)
         print(sentence.sentiment)
         print(sentence.correct())
         print(datum_box.twitter_sentiment_analysis(sentence))
         print(datum_box.is_adult_content(sentence))
         response = alchemyapi2.language('text', blob)

         if response['status'] == 'OK':
            print('## Response Object ##')
            print(json.dumps(response, indent=4))

            print('')
            print('## Language ##')
            print('language: ', response['language'])
            print('iso-639-1: ', response['iso-639-1'])
            print('native speakers: ', response['native-speakers'])
            print('')
         else:
            print('Error in language detection call: ', response['statusInfo'])

         response = alchemyapi2.taxonomy('text', blob)

         if response['status'] == 'OK':
            print('## Response Object ##')
            print(json.dumps(response, indent=4))

            print('')
            print('## Categories ##')
            for category in response['taxonomy']:
                print(category['label'], ' : ', category['score'])
            print('')

         else:
            print('Error in taxonomy call: ', response['statusInfo'])

         response = alchemyapi2.sentiment('text', blob)

         if response['status'] == 'OK':
            print('## Response Object ##')
            print(json.dumps(response, indent=4))

            print('')
            print('## Targeted Sentiment ##')
            print('type: ', response['docSentiment']['type'])

            if 'score' in response['docSentiment']:
                print('score: ', response['docSentiment']['score'])
         else:
            print('Error in targeted sentiment analysis call: ',
                  response['statusInfo'])

         response = alchemyapi2.keywords('text', blob, {'sentiment': 1})

         if response['status'] == 'OK':
            print('## Response Object ##')
            print(json.dumps(response, indent=4))

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
