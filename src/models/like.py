from datetime import datetime

from config import db, ma


class Like(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class LikeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Like
        load_instance = True
        sqla_session = db.session
        include_fk = True


like_schema = LikeSchema() 

