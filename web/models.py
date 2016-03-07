import datetime
from app import db

class Message(db.Model):
    __tablename__ = 'messages'
    msgId = db.Column('messageSid', db.String, primary_key=True)
    msgFrom = db.Column(db.String(20))
    msgTo = db.Column(db.String(20))
    msgBody = db.Column(db.String(1600))
    date_posted = db.Column(db.DateTime, nullable=False)

    def __init__(self, msgId, msgFrom, msgTo, msgBody):
        self.msgId = msgId
        self.msgFrom = msgFrom
        self.msgTo = msgTo
        self.msgBody = msgBody
        self.date_posted = datetime.datetime.now()
