from enum import Enum


class Sender(Enum):
    APPLICANT = 'Applicant'
    INTERVIEWER = 'Interviewer'
    AI = 'AI'

s = Sender.APPLICANT
print(s)
print((type(Sender.APPLICANT)))