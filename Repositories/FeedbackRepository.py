from models import Feedback
from db import db


def insertFeedback(feedback, userId):
    feedback = Feedback(feedback=feedback, createdBy=userId)
    db.session.add(feedback)
    db.session.commit()
