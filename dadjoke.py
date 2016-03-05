# import twilio.twiml, json
from random import randint
from flask import Flask, request, flash, redirect, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:flaskpass@198.199.65.115:5432/flaskdb'
db = SQLAlchemy(app)

# cue the deer
with open('jokes.json') as json_data_file:
    jokes = json.load(json_data_file)


class Message(db.Model):
    __tablename__ = "messages"
    msgId = db.Column('messageSid', db.String, primary_key=True)
    msgFrom = db.Column(db.String(20))
    msgTo = db.Column(db.String(20))
    msgBody = db.Column(db.String(1600))
    pub_date = db.Column(db.DateTime)

    def __init__(self, msgID, msgFrom, msgTo, msgBody):
        self.msgId = msgId
        self.msgFrom = msgFrom
        self.msgTo = msgTo
        self.msgBody = msgBody
        self.pub_date = datetime.utcnow()

db.create_all()


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html',
            messages = Message.query.order_by(Message.pub_date.desc()).all()
        )

# @app.route('/joke', methods=['GET', 'POST'])
# def dadjoke_ready():
#     txt = request.values.get('Body').lower()
#     dad_joke = ['dad joke', 'dadjoke', 'dad-joke']
#     #if txt is received asking for a dad joke
#     if any(x in txt for x in dad_joke):
#         resp = twilio.twiml.Response()
#         resp.sms(jokes[randint(0,len(jokes)-1)])

#         message = Message(request.values.get('MessageSid'), request.values.get('From'),
#             request.values.get('To'), request.values.get('Body'))
#         db.session.add(message)
#         db.session.commit()

#         return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', threaded=True)
