from flask import abort
from models.user import User, user_schema, users_schema
from utils.update_last_iteraction import update_last_iteraction


@update_last_iteraction
def get_all():
    users = User.query.all()
    return users_schema.dump(users)


@update_last_iteraction
def get_one(username: str):
    user = User.query.filter(User.username == username).one_or_none()

    if user is not None:
        return user_schema.dump(user)
    else:
        abort(404, f"User with username {username} not found")

