from flask import Blueprint, request, jsonify

from app import db, http_auth
from app.models.post import Post
from app.models.user import User
from app.forms import BasicForm
from sqlalchemy import desc
import datetime

bp = Blueprint("api_bp", __name__)

# @bp.route('/posts', methods=['GET'])
@bp.get('/posts')
def search_posts():
    posts = Post.query.all()
    return jsonify({"posts": [post.to_dict() for post in posts]}), 200

@bp.get('/posts/<id>')
def get_post(id):
    post = Post.query.get(id)
    return jsonify({'post': post.to_dict()}), 200

# @bp.route('/posts', methods=['POST'])
@bp.post('/posts')
@http_auth.login_required
def create_post():
    user = http_auth.current_user()
    post = Post()
    post.from_dict(request.json)
    post.user = user # post.user_id = user.id
    db.session.add(post)
    db.session.commit()
    return jsonify({'post': post.to_dict()}), 201

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
