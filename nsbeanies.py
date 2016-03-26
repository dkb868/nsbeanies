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
from flask import Flask, session, redirect, url_for, escape, request
from textblob import TextBlob
from DatumBox import DatumBox
import json
import requests
import alchemyapi


app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/list_channels/')
def list_channels():
    channels = ['UCqpDX3iK-C8rM_AfsXMcFQQ']
    return render_template('list_channels.html', channels=channels)


# route to get all the stats for one channel
@app.route('/get_stats/<channelId>')
def get_stats(channelId):
    sentiments = db.nsbeanie_sentiments.find()
    total = 0
    positive = 0
    negative = 0
    adult = 0
    polarity = 0.6
    subjectivity = 160

    # above ^ temporarily* hardcoded

    for sentiment in sentiments:
        total += 1
        s =  sentiment['twitter']
        if (s == 'positive'):
            positive+=0.2
        elif (s == 'negative'):
            negative+=12

        a = sentiment['adult']
        if(a=='True'):
            adult += 1
            print "Adult works? OL"

    sentiment = {
        "positive": positive,
        "negative": negative,
        "adult" : adult,
        "polarity": polarity,
        "subjectivity": subjectivity,
        "total" : total
    }

    # Download the twilio-python library from http://twilio.com/docs/libraries
    from twilio.rest import TwilioRestClient

    # Find these values at https://twilio.com/user/account
    account_sid = "AC74d3f913d8417e3da6fe763e7119db38"
    auth_token = "3efc44c6e1aa92a223d77e6445bcf5ed"
    client = TwilioRestClient(account_sid, auth_token)

    message = client.messages.create(to="+14804943646", from_="+12028499415",
                                         body="Your child may be a victim of cyberbullying, go to beanie's website for more information. ")


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
    return render_template('channel_stats.html', sentiment=sentiment, sentiments=sentiments)

# route to post a channel
@app.route('/add_channel/', methods=['GET', 'POST'])
def add_channel():
    if(request.method == 'POST'):
        channelLink = request.form['channelLink']
        channelId = channelLink.split('/')[-1]
        print channelId
        comments = requests.get('https://www.googleapis.com/youtube/v3/commentThreads?allThreadsRelatedToChannelId=' + channelId + '&key=AIzaSyCxZaTTMnBXzqqlNztjRyVktS9yT8Oyo7Q&part=snippet')
        comments = comments.json()
        for item in comments['items']:
            print item['snippet']['topLevelComment']['snippet']['textDisplay']
            print item['snippet']['videoId']
            text = item['snippet']['topLevelComment']['snippet']['textDisplay']
            videoId = item['snippet']['videoId']
            channelId = item['snippet']['channelId']
            comment = {
                "text": text,
                "videoId": videoId,
                "channelId": channelId
            }

            db.nsbeanie_comments.insert_one(comment)
            print "succesfully inserted"

        print "Succesfully added to DB"

        ################################
        #SENTIMENT ANALYSIS#
        ##########################
        print "ABOUT TO DO SENTIMENT ANALYSIS"

        #alchemyapi.apikey = 'de78af95d7e36a826fe4164c7b7fe5763cdbacdf'

        # Datum Box API_KEY
        API_KEY = "950ac57f58cc94268ac3cf43161c736b"
        datum_box = DatumBox(API_KEY)


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
                 print "succesfully inserted SENTIMENT"




        print "DONE ALL PROCESSING SUCCESFULY"

        return redirect('/get_stats/' + channelId)
    return render_template('add_channel.html')



if __name__ == '__main__':
    app.debug = True
    app.run()
