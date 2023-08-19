from flask import abort
from config import db
from models.post import Post, post_schema, posts_schema


def get_all():
    posts = Post.query.all()
    return posts_schema.dump(posts)


def get_one(post_id: int):
    post = Post.query.filter(Post.id == post_id).one_or_none()

    if post is not None:
        return post_schema.dump(post)
    else:
        abort(404, f"Post with username {post_id} not found")


def create(post, token_info):
    post["user_id"] = token_info["user_id"]
    new_post = post_schema.load(post, session=db.session)
    db.session.add(new_post)
    db.session.commit()

    return post_schema.dump(new_post), 201

