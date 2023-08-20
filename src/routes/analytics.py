from datetime import datetime
from flask import make_response
from sqlalchemy import and_

from config import app
from models.like import Like

def count_likes_for_period(date_from: str, date_to: str):

    start = datetime.strptime(date_from, "%Y-%m-%d").date()
    end = datetime.strptime(date_to, "%Y-%m-%d").date()

    likes = Like.query.filter(and_(
            Like.date_of_creation >= start,
            Like.date_of_creation <= end
        )).count()

    return make_response({ "likes" : likes }, 200)

