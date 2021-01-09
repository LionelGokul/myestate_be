from flask import request
import json
from Repositories.FeedbackRepository import insertFeedback


def feedback():
    try:
        data = request.get_json()
        print(data)
        insertFeedback(data['feedback'], data['userId'])
        return 'success', 200
    except Exception as e:
        return json.dumps(e), 500
