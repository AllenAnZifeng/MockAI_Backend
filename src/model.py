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
class Response:
    def __init__(self, status: bool, data):
        self.status = status
        self.data = data

    def to_dict(self):
        return {
            'status': self.status,
            'data': self.data
        }