from datetime import datetime
from flask import abort, make_response
from sqlalchemy import and_

from models.like import Like

def count_likes_for_period(date_from: str, date_to: str):

    try:
        start = datetime.strptime(date_from, "%Y-%m-%d").date()
        end = datetime.strptime(date_to, "%Y-%m-%d").date()
    except ValueError:
        abort(400, "Date in wrong format.")

    likes = Like.query.filter(and_(
            Like.date_of_creation >= start,
            Like.date_of_creation <= end
        )).count()

    return make_response({ "likes" : likes }, 200)

