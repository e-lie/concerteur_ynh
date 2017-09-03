from app import db
from sqlalchemy.sql import func
from datetime import datetime

class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)

    #ajust the datetime entry from the clock of the db server. Better because it can be different from the app server's one
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    title = db.Column(db.Unicode(300))
    text = db.Column(db.Unicode(1000))
    current = db.Column(db.Boolean())
    archive_name = db.Column(db.Unicode(300))
    audio_path = db.Column(db.String(500))
    trashed = db.Column(db.Boolean(), default=False)

    messages = db.relationship('Message', backref='question')


    def __init__(self, text, title, current):
        self.text = text
        self.title = title
        self.current = current

    def __repr__(self):
        return '<Question {}: {}>'.format(self.id, self.text)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    numHash = db.Column(db.String(100))
    messages = db.relationship('Message', backref='user')

    def __init__(self, numHash, message):
        self.numHash = numHash
        self.messages = [message]

    def __repr__(self):
        return '<User {}: {}>'.format(self.id, self.numHash)

class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    
    #ajust the 7datetime entry from the clock of the db server. Better because it can be different from the app server's one
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    text = db.Column(db.Unicode(1000))
    audio_path = db.Column(db.String(500))
    trashed = db.Column(db.Boolean(), default=False)

    def __init__(self, text, question_id):
        self.text = text
        self.question_id = question_id

    def __repr__(self):
        return '<Message {}: {}>'.format(self.id, self.text)
