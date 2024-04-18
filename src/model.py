from datetime import datetime
from enum import Enum

from .database import db


class Interview(db.Model):
    interview_id = db.Column(db.Integer, primary_key=True)
    candidate_name = db.Column(db.String(100), nullable=False)
    interviewer_name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    comments = db.Column(db.Text)

    def __init__(self, candidate_name, interviewer_name, date, comments):
        self.candidate_name = candidate_name
        self.interviewer_name = interviewer_name
        self.date = date
        self.comments = comments

    def __repr__(self):
        return f'<Interview: {self.candidate_name=} {self.interviewer_name=} {self.date=} {self.comments=}>'

    def to_dict(self):
        return {
            'id': self.interview_id,
            'candidateName': self.candidate_name,
            'interviewerName': self.interviewer_name,
            'date': self.date.strftime("%Y-%m-%d %H:%M:%S"),
            'comments': self.comments
        }





class Chat(db.Model):
    chat_id = db.Column(db.Integer, primary_key=True)
    interview_id = db.Column(db.Integer, db.ForeignKey('interview.interview_id'), nullable=False)
    sender = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, interview_id, sender, message):
        self.interview_id = interview_id
        self.sender = sender
        self.message = message

    def __repr__(self):
        return f'<Chat {self.chat_id}: {self.sender} says "{self.message}" on {self.timestamp}>'

    def to_dict(self):
        return {
            'chatID': self.chat_id,
            'interviewID': self.interview_id,
            'sender': self.sender,
            'message': self.message,
            'timestamp': self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }


class Response:
    def __init__(self, status: bool, data):
        self.status = status
        self.data = data

    def to_dict(self):
        return {
            'status': self.status,
            'data': self.data
        }
