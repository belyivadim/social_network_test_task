from datetime import datetime
from config import db, ma


class Post(db.Model):
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    content = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class PostSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Post
        load_instance = True
        sqla_session = db.session
        include_fk = True


post_schema = PostSchema()
posts_schema = PostSchema(many=True)
