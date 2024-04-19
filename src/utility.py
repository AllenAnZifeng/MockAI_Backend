import base64
from typing import List

import requests

with open('src/secret.txt') as f:
    api_key = f.read().strip()

domain = 'localhost'

def get_ai_feedback(images: List[str],previous_feedback:str):
    content = [{
        "type": "text",
        "text": "All drawings from the applicant, and feedback from ChatGPT are given in chronological order from the earliest to the latest."
                "Give feedback on the latest drawing, focus on the difference with the previous drawing."
                "Here are the previous feedbacks." + previous_feedback
    }]

    for image in images:
        content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/png;base64,{image}"
            }
        })

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4-turbo",
        "messages": [
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": "You are an interviewer for a software engineer position.Question is to design a parking lot system."
                                "The applicant will draw the design diagrams on the whiteboard. "
                                "You need to provide feedback on the design and keep prompting the applicant to add details."
                                "Make sure your response is concise and clear."
                                "You may decide when to end the interview."
                    }
                ]
            },
            {
                "role": "user",
                "content": content
            }
        ],
        "max_tokens": 200
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    return response.json()

