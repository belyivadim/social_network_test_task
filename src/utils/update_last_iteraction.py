from datetime import datetime
from collections.abc import Callable
from functools import wraps

from flask import abort, g

from config import db
from models.user import User


def update_last_iteraction(f) -> Callable:
    @wraps(f)
    def decorator_func(*args, **kwargs):
        try:
            user_id = g.token_info['user_id']
        except AttributeError:
            abort(401, "Unauthorized.")
        
        user = User.query.filter(User.id == user_id).one_or_none()

        if user is None:
            abort(401, "Unauthorized.")

        user.last_iteraction = datetime.utcnow()
        db.session.merge(user)
        db.session.commit()

        return f(*args, **kwargs)

    return decorator_func


