from flask import make_response
from sqlalchemy import and_

from models.like import Like, like_schema
from config import db

def like_post(post_id: int, token_info):
    user_id = token_info['user_id']
    existing_like = Like.query.filter(and_(
            Like.user_id == user_id,
            Like.post_id == post_id
        )).one_or_none()

    if existing_like is not None:
        db.session.delete(existing_like)
        db.session.commit()
        return make_response("Post successfully unliked", 200)
    else:
        new_like = { "user_id": user_id, "post_id": post_id }
        new_like = like_schema.load(new_like, session=db.session)
        res = db.session.add(new_like)
        db.session.commit()
        return like_schema.dump(res), 201

