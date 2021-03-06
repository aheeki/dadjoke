import datetime
import simplejson as json
from datetime import timedelta
from app import db

class Message(db.Model):
    __tablename__ = 'messages'
    msgId = db.Column('messageSid', db.String, primary_key=True)
    msgFrom = db.Column(db.String(20))
    msgBody = db.Column(db.String(1600))
    dadjoke = db.Column(db.Boolean)
    date_posted = db.Column(db.DateTime, nullable=False)

    def __init__(self, msgId, msgFrom, msgBody, dadjoke):
        self.msgId = msgId
        self.msgFrom = msgFrom
        self.msgBody = msgBody
        self.dadjoke = dadjoke
        self.date_posted = datetime.datetime.now()-timedelta(hours=5)

    def __repr__(self):
        return json.dumps({"msgId": self.msgId, "msgFrom": self.msgFrom, "msgBody": self.msgBody, "dadjoke": self.dadjoke, "date_posted": self.date_posted.isoformat()})

    @property
    def serialize(self):
        return {"msgId": self.msgId, "msgFrom": self.msgFrom, "msgBody": self.msgBody, "dadjoke": self.dadjoke, "date_posted": self.date_posted.isoformat()}
