from datetime import datetime
from time import time
from flask import abort, g
from jose import JWTError, jwt
from werkzeug.exceptions import Unauthorized
from models.user import User, user_schema

from config import db, app


JWT_SECRET = app.config["JWT_SECRET"]
JWT_LIFETIME_IN_SECONDS = int(app.config["JWT_LIFETIME_IN_SECONDS"])
JWT_ALGORITHM = app.config["JWT_ALGORITHM"]


def signin(user: dict):
    username = user["username"]
    password = user["password"]

    existing_user = User.query.filter(User.username == username).one_or_none()

    if existing_user is None or existing_user.password != password:
        abort(401, "Wrong username or password")

    existing_user.last_login = datetime.utcnow()
    db.session.merge(existing_user)
    db.session.commit()

    user_id = existing_user.id
    ts = int(time())
    payload = {
            "iat": ts,
            "exp": ts + JWT_LIFETIME_IN_SECONDS,
            "user_id": str(user_id)
        }

    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return { "token": token }, 200


def signup(user):
    username = user.get("username")

    existing_user = User.query.filter(User.username == username).one_or_none()

    if existing_user is not None:
        abort(409, f"User with username {username} already exists")

    new_user = user_schema.load(user, session=db.session)
    db.session.add(new_user)
    db.session.commit()

    return user_schema.dump(new_user), 201


def decode_token(token: str):
    try:
        g.token_info = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return g.token_info
    except JWTError as e:
        raise Unauthorized from e
