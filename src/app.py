import base64

from flask import Flask, request, jsonify

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from src.model import Interview, Response, Chat, Screenshot
from src.database import db
from flask_cors import CORS
from datetime import datetime

from src.utility import get_ai_feedback, frontend_domain
from pyvirtualdisplay import Display

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

# display = Display(visible=False, size=(1024, 768))
# display.start()
@app.route('/')
def hello_world():
    return 'Hello World!'


def page_has_loaded(driver):
    return driver.execute_script(
        "return typeof window.exportToBlob !== 'undefined' && window.exportToBlob !== null && window.editor !== null;")


@app.get('/feedback/<roomID>')
def get_feedback(roomID):
    response = get_draw_board_data(roomID)
    if not response[0]:
        return jsonify(Response(False, 'Error or unexpected result').to_dict())
    else:
        image_base64_for_api = response[1]
        # print(image_base64_for_api)
        # add image data to db
        img = Screenshot(int(roomID), image_base64_for_api)
        db.session.add(img)
        db.session.commit()

        # get all images for the roomID sort by timestamp
        screenshots = Screenshot.query.filter_by(interview_id=int(roomID)).order_by(Screenshot.timestamp).all()

        # get previous feedback from AI
        previous_chats = Chat.query.filter_by(interview_id=int(roomID), sender='AI').order_by(Chat.timestamp).all()
        previous_feedback = '\n'.join([chat.message for chat in previous_chats][-20:])  # only keep the last 20 feedbacks
        obj = get_ai_feedback([img.image for img in screenshots], previous_feedback)

        feedback = obj['choices'][0]['message']['content']

        # add feedback to chat
        new_chat = Chat(
            interview_id=int(roomID),
            sender='AI',
            message=feedback
        )
        db.session.add(new_chat)
        db.session.commit()

        return jsonify(Response(True, feedback).to_dict())





def get_draw_board_data(roomID): # internal function
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--remote-debugging-pipe')
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_argument('--disable-dev-shm-usage')
    # chrome_options.add_argument("--window-size=1024,768")

    print('1')
    driver = webdriver.Chrome(options=chrome_options)
    print('2')
    driver.get(f'{frontend_domain}/internal/{roomID}')
    print('3')
    WebDriverWait(driver, 5).until(page_has_loaded)
    print('4')


    result = driver.execute_script("""
             return ( async () => {
                try {
                    const blob = await window.exportToBlob();
                    return new Promise((resolve, reject) => {
                    const reader = new FileReader();
                    reader.onloadend = () => resolve(reader.result);
                    reader.onerror = reject;
                    reader.readAsDataURL(blob);
            });
                } catch (error) {
                    return { error: error.message };
                }
            })();
            """)

    if isinstance(result, str) and result.startswith("data:image/png;base64,"):
        base64_encoded = result.split(',', 1)[1]
        image_data = base64.b64decode(base64_encoded)
        image_base64_for_api = base64.b64encode(image_data).decode('utf-8')
        print('got image',len(image_base64_for_api))
        driver.quit()

        return True, image_base64_for_api
    else:
        driver.quit()
        print('did not get image')
        return False, 'Error or unexpected result'


@app.get('/verify/<roomID>')
def verify_roomID(roomID):
    result = Interview.query.get(int(roomID))
    if result is not None:
        return jsonify(Response(True, 'Room ID is valid').to_dict())
    else:
        return jsonify(Response(False, 'Room ID is invalid').to_dict())


@app.get('/interviews')
def get_interviews():
    interviews = Interview.query.all()
    print(interviews)
    interviews_list = [interview.to_dict() for interview in interviews]
    return jsonify(Response(True, interviews_list).to_dict())


@app.get('/chats/<roomID>')
def get_chats(roomID):
    # sort by timestamp
    chats = Chat.query.filter_by(interview_id=int(roomID)).order_by(Chat.timestamp).all()
    # print(chats)
    chats_list = [chat.to_dict() for chat in chats]
    return jsonify(Response(True, chats_list).to_dict())


@app.post('/chats')
def send_chats():
    if request.is_json:
        data = request.get_json()

        interview_id = data['roomID']
        sender = data['sender']
        message = data['message']

        new_chat = Chat(
            interview_id=interview_id,
            sender=sender,
            message=message
        )
        db.session.add(new_chat)
        db.session.commit()
        print('added', new_chat)
        return jsonify(Response(True, 'Chat added successfully').to_dict())

    else:
        return jsonify(Response(False, 'Invalid Request. Not JSON').to_dict())


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
        print(new_interview.interview_id)
        new_chat = Chat(
            interview_id=new_interview.interview_id,
            sender='Admin',
            message='Design a parking lot system. Draw the design diagrams on the whiteboard. The AI system will judge and provide you with further guidance.'
        )
        db.session.add(new_chat)
        db.session.commit()
        print('added', new_interview)
        return jsonify(Response(True, 'Interview added successfully').to_dict())

    else:
        return jsonify(Response(False, 'Invalid Request. Not JSON').to_dict())


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=16000,debug=True)
