import json

from flask import Flask, request, jsonify
from src.model import Interview, Response
from src.database import db
from flask_cors import CORS
from datetime import datetime


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yourdatabase.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()  # Create SQL tables for our data models

    return app


app = create_app()
CORS(app)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.get('/interviews')
def get_interviews():
    interviews = Interview.query.all()
    print(interviews)
    interviews_list = [interview.to_dict() for interview in interviews]
    return jsonify(Response(True, interviews_list).to_dict())


@app.post('/interviews')
def send_interviews():
    if request.is_json:
        data = request.get_json()

        candidateName = data['candidateName']
        interviewerName = data['interviewerName']
        date = data['date']
        comments = data['comments']

        if len(candidateName) == 0:
            print('Candidate Name cannot be empty')
            return jsonify(Response(False, 'Candidate Name cannot be empty').to_dict())

        date_object = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

        new_interview = Interview(
            candidate_name=candidateName,
            interviewer_name=interviewerName,
            date=date_object,
            comments=comments
        )
        db.session.add(new_interview)
        db.session.commit()
        print('added', new_interview)
        return jsonify(Response(True, 'Interview added successfully').to_dict())

    else:
        return jsonify(Response(False, 'Invalid Request. Not JSON').to_dict())



if __name__ == '__main__':
    app.run(debug=True)
