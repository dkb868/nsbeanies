# Nsbe Hacakathon 42
# Beanies
# Youtube Kids App detection
# For educational use for cool people
# Website will be added

from alchemyapi import AlchemyAPI
from pymongo import MongoClient
client = MongoClient('mongodb://mitrikyle:Allthatiknow1@ec2-52-11-150-10.us-west-2.compute.amazonaws.com:27017')
db = client.dummyDB
from textblob import TextBlob
from DatumBox import DatumBox
import json
from flask import Flask, render_template, request, make_response
from authomatic.adapters import WerkzeugAdapter
from authomatic import Authomatic
import authomatic.providers.oauth2 as oauth2

app = Flask(__name__)
# Datum Box API_KEY
API_KEY = "950ac57f58cc94268ac3cf43161c736b"
datum_box = DatumBox(API_KEY)
alchemyapi2 = AlchemyAPI()



CONFIG = {
    'google': {
        'class_': oauth2.Google,
        'consumer_key': '########################',
        'consumer_secret': '########################',
        'scope': oauth2.Google.user_info_scope + ['https://www.googleapis.com/youtube/v3/'],
    },
}

authomatic = Authomatic(CONFIG, 'random secret string for session signing')


@app.route('/login/<provider_name>/', methods=['GET', 'POST']) # provider_name = "google"
def login(provider_name):
    response = make_response()

    # Authenticate the user
    result = authomatic.login(WerkzeugAdapter(request, response), provider_name)

    if result:
        videos = []
        if result.user:
            # Get user info
            result.user.update()

            # Talk to Google YouTube API
            ## get the phone number somewhere here?? idk? take their phone number then open the auth page????
            if result.user.credentials:
                response = result.provider.access('https://www.googleapis.com/youtube/v3/channels?part=contentDetails&mine=true')
                if response.status == 200:
                        for item in response.data.get('items', []):
                            if not db.nsbeanie_users.find_one(item.get("id", "")):
                                userDic = {
                                    "_id": item.get("id", ""),
                                    "phone" : "",
                                }
                            else:
                                pass ## cause i guess there's nothing really left to do.
                    ## I'm assuming there's a system that's connecting channel IDs with phone numbers.
                ## Schema = {channelID: x, phone: y}

        return render_template() # phone num and whatever in here
    return response




import smtplib
userAddress ="postmaster@sandboxf32a8e5d26ea4769a1e20168754971a5.mailgun.org"
userPassword ="8e14d70dd060c158212a4f7b438f7b79"
server = smtplib.SMTP('smtp.mailgun.org', 587)
server.starttls()
server.login(userAddress, userPassword)

msg = "YOUR MESSAGE!"
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
