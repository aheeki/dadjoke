import twilio.twiml, json, random
from redis import Redis
from flask import Flask, request, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from config import BaseConfig

app = Flask(__name__)
app.config.from_object(BaseConfig)
db = SQLAlchemy(app)
redis = Redis()


#cue the jokes
with open('jokes.json') as json_data_file:
    jokes = json.load(json_data_file)

from models import *

@app.route('/', methods=['GET'])
def index():
    messages = Message.query.order_by(Message.date_posted.desc()).all()
    return render_template('index.html', messages=messages)

@app.route('/joke', methods=['POST'])
def dadjoke_ready():
    redis.incr('jokesTold')
    print(redis.get('jokesTold'))
    txt = request.values.get('Body')
    dad_joke = ['dad joke', 'dadjoke', 'dad-joke']
    #if txt is received asking for a dad joke
    if any(x in txt.lower() for x in dad_joke):
        senderNum = request.values.get('From')

        resp = twilio.twiml.Response()
        resp.sms(newJoke(senderNum))

        message = Message(request.values.get('MessageSid'), senderNum, txt)
        db.session.add(message)
        db.session.commit()

        return str(resp)

def newJoke(phoneNum):
    joke = random.choice(jokes)
    return joke


if __name__ == '__main__':
    app.run()    
