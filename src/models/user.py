from datetime import datetime
from marshmallow_sqlalchemy import fields

from config import db, ma
from .post import Post, PostSchema


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(32))
    last_iteraction = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship(
            Post,
            backref="person",
            cascade="all, delete, delete-orphan",
            single_parent=True,
            order_by="desc(Post.created_at)"
        )


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        sqla_session = db.session
        include_relationship = True

    posts = fields.Nested(PostSchema, many=True)


user_schema = UserSchema()
users_schema = UserSchema(many=True)
