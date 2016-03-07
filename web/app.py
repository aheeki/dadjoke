import twilio.twiml, json
from random import randint
from flask import Flask, request, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from config import BaseConfig


app = Flask(__name__)
app.config.from_object(BaseConfig)
db = SQLAlchemy(app)

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
    txt = request.values.get('Body').lower()
    dad_joke = ['dad joke', 'dadjoke', 'dad-joke']
    #if txt is received asking for a dad joke
    if any(x in txt for x in dad_joke):
        resp = twilio.twiml.Response()
        resp.sms(jokes[randint(0,len(jokes)-1)])

        message = Message(request.values.get('MessageSid'), request.values.get('From'),
            request.values.get('To'), request.values.get('Body'))
        db.session.add(message)
        db.session.commit()

        return str(resp)


if __name__ == '__main__':
    app.run()    
