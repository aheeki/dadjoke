import twilio.twiml, json, random, datetime
from twilio.rest import TwilioRestClient
from datetime import timedelta
from redis import Redis
from flask import Flask, request, render_template, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.cors import CORS
from config import BaseConfig


app = Flask(__name__)
app.config.from_object(BaseConfig)
db = SQLAlchemy(app)
cors = CORS(app)
redis = Redis(host='redis', port=6379)
client = TwilioRestClient(app.config["ACCOUNT_SID"], app.config["AUTH_TOKEN"])


#cue the jokes
with open('jokes.json') as json_data_file:
    jokes = json.load(json_data_file)


from models import *

@app.route('/jokeWeb', methods=['POST'])
def jokeWeb():
    phone = request.values.get('phone')
    joke = newJoke(phone)
    resp = client.messages.create(to=phone, from_=app.config["TWILIO_PHONE"], body=joke)
    message = Message(resp.sid, phone, '', True)    
    db.session.add(message)
    db.session.commit()    
    return str(resp)

@app.route('/joke', methods=['POST'])
def dadjoke_ready():
    txt = request.values.get('Body')
    senderNum = request.values.get('From')    
    dad_joke = ['dad joke', 'dadjoke', 'dad-joke']
    resp = twilio.twiml.Response()
    #if txt is received asking for a dad joke
    if any(x in txt.lower() for x in dad_joke):
        message = Message(request.values.get('MessageSid'), senderNum, txt, True)
        resp.sms(newJoke(senderNum))
    else:
        message = Message(request.values.get('MessageSid'), senderNum, txt, False)        
    db.session.add(message)
    db.session.commit()
    return str(resp)

def newJoke(phoneNum):
    # check if all jokes have already been told to phoneNum
    if (redis.scard(phoneNum+'_timestamp')==len(jokes)):
        return 'Dad\'s out of jokes. Send in your own: andrewheekin@gmail.com'
    # create a new set [0, 1...len(jokes)] if not already exists
    if (redis.exists(phoneNum)==False):
        redis.sadd(phoneNum, *range(len(jokes)))
    # return a random joke number then remove it
    rand = redis.spop(phoneNum)
    print('Phone number: ', phoneNum, ', ', 'popped: ',
        rand, ', ', 'joke set: ', redis.smembers(phoneNum))
    # track the timestamps
    redis.sadd(phoneNum+'_timestamp', [rand, datetime.datetime.now()-timedelta(hours=5)])    
    rand = int(rand)
    # \n puts line break in sms
    return jokes[rand] + '\n\n👔http://dadjokebot.com'

@app.route('/pageviews', methods=['GET'])
def getPageviews():
    return jsonify({"pageviews":int(redis.get('pageViews'))})

@app.route('/jokestold', methods=['GET'])
def getJokesTold():
    redis.incr('pageViews')    
    results = []
    messages = Message.query.order_by(Message.date_posted.desc()).all()
    for message in messages:
        results.append(message.serialize)
    return jsonify(jokesTold = results)



if __name__ == '__main__':
    app.run()    
