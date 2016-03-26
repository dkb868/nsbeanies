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
from email.mime.text import MIMEText

userAddress ="postmaster@sandboxf32a8e5d26ea4769a1e20168754971a5.mailgun.org"
userPassword ="8e14d70dd060c158212a4f7b438f7b79"

msg = MIMEMultipart('alternative')
msg['Subject'] = 'Beanies Updates - Potential '
msg['From'] = userAddress
msg['To'] = 'krystal.folkes@gmail.com'
# Create the body of the message (a plain-text and an HTML version).

html = """\
<html>


<head>
  <title>Beanies</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.0/jquery.min.js"></script>
  <script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"></script>
</head>
<body>

<div class="container">
  <div class="jumbotron">
    <h1>Beanies Notification</h1>

    <p>Hello,<br>
     <p> We would like to inform you that your child may be a potential victim of Cyberbullying. </p>
       Login to  <a href="http://localhost:5000">Beanies</a> for more information
    </p>
  </div>
  <p>Thanks.</p>
<br>
<br>
<br>
<p>Beanies</p>
  <p>"Reduce the trend of Cyberbullying for YouTube Kids".</p>
</div>

</body>




</html>
"""

part2 = MIMEText(html, 'html')

# Attach parts into message container.
# According to RFC 2046, the last part of a multipart message, in this case
# the HTML message, is best and preferred.

msg.attach(part2)

server = smtplib.SMTP('smtp.mailgun.org', 587)
server.ehlo()
server.starttls()

server.login(userAddress, userPassword)
server.sendmail(userAddress,"krystal.folkes@gmail.com", msg.as_string())
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
