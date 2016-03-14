import twilio.twiml, json, random
import datetime
from datetime import timedelta
from redis import Redis
from flask import Flask, request, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from config import BaseConfig


app = Flask(__name__)
app.config.from_object(BaseConfig)
db = SQLAlchemy(app)
redis = Redis(host='redis', port=6379)


#cue the jokes
with open('jokes.json') as json_data_file:
    jokes = json.load(json_data_file)


from models import *


@app.route('/', methods=['GET'])
def index():
    redis.incr('pageViews')
    messages = Message.query.order_by(Message.date_posted.desc()).all()
    return render_template('index.html', messages=messages, pageviews=int(redis.get('pageViews')))

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
    # convert string to int
    rand = int(rand)
    return jokes[rand]


if __name__ == '__main__':
    app.run()    
