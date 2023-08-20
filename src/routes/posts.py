from flask import abort

from config import db
from models.post import Post, post_schema, posts_schema
from utils.update_last_iteraction import update_last_iteraction


@update_last_iteraction
def get_all():
    posts = Post.query.all()

    for post in posts:
        post.likes_count = post.get_post_likes_count()

    return posts_schema.dump(posts)


@update_last_iteraction
def get_one(post_id: int):
    post = Post.query.filter(Post.id == post_id).one_or_none()

    if post is not None:
        post.likes_count = post.get_post_likes_count()
        return post_schema.dump(post)
    else:
        abort(404, f"Post with username {post_id} not found")


@update_last_iteraction
def create(post, token_info):
    post["user_id"] = token_info["user_id"]
    new_post = post_schema.load(post, session=db.session)
    db.session.add(new_post)
    db.session.commit()

    return post_schema.dump(new_post), 201

