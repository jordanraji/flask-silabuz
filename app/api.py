from flask import Blueprint, request, jsonify

from app import db, http_auth
from app.models.post import Post
from app.models.user import User
from app.forms import BasicForm
from sqlalchemy import desc
import datetime
from app.schemas.post import post_schema, posts_schema
from app.schemas.user import user_schema

bp = Blueprint("api_bp", __name__)

# @bp.route('/posts', methods=['GET'])
@bp.get('/posts')
def search_posts():
    posts = Post.query.all()
    # return jsonify({"posts": [post.to_dict() for post in posts]}), 200
    return posts_schema.dump(posts)

@bp.get('/posts/<id>')
def get_post(id):
    post = Post.query.get(id)
    # return jsonify({'post': post.to_dict()}), 200
    return post_schema.dump(post)

# @bp.route('/posts', methods=['POST'])
@bp.post('/posts')
@http_auth.login_required
def create_post():
    # user = http_auth.current_user()
    # post = Post()
    # post.from_dict(request.json)
    # post.user = user # post.user_id = user.id
    # db.session.add(post)
    # db.session.commit()
    # return jsonify({'post': post.to_dict()}), 201
    post = post_schema.load(request.json)
    post.user = http_auth.current_user()
    db.session.add(post)
    db.session.commit()
    return post_schema.dump(post)


# @bp.route('/posts/<id>', methods=["PUT"])
@bp.put('/posts/<id>')
@http_auth.login_required
def update_post(id):
    post = Post.query.get(id)
    user = http_auth.current_user()
    if post.user_id == user.id:
        post.from_dict(request.json)
        # post.timestamp = datetime.datetime.utcnow
        db.session.commit()
        return jsonify({"post": post.to_dict()}), 201
    return jsonify({"error": "There was an error!"}), 400

# @bp.route('/posts/<id>', methods=["DELETE"])
@bp.delete('/posts/<id>')
@http_auth.login_required
def delete_post(id):
    post = Post.query.get(id)
    user = http_auth.current_user()
    if post.user_id == user.id:
        db.session.delete(post)
        db.session.commit()
        return jsonify({"message": "Your post has been deleted successfully"}), 200
    return jsonify({"error": "There was an error!"}), 400

@bp.get('/users/<id>')
def get_user(id):
    user = User.query.get(id)
    return user_schema.dump(user)
