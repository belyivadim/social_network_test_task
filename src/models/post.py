from datetime import datetime
from sqlalchemy import func

from marshmallow import fields
from sqlalchemy.orm import object_session
from config import db, ma
from models.like import Like


class Post(db.Model):
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    content = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    likes_count = 0

    def get_post_likes_count(self) -> int:
        return Like.query.filter(Like.post_id == self.id).count()


class PostSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Post
        load_instance = True
        sqla_session = db.session
        include_fk = True

    likes_count = fields.Method("get_likes_count")

    def get_likes_count(self, obj) -> int:
        return obj.likes_count
        
        
post_schema = PostSchema()
posts_schema = PostSchema(many=True)
