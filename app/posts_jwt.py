from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, current_user

from app.models.post import Post
from app.models.user import User
from app.forms import BasicForm
from sqlalchemy import desc
from app import db, jwt
import datetime

bp = Blueprint("posts_jwt_bp", __name__)


@bp.post('/login')
def login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        expires = datetime.timedelta(days=1)
        access_token = create_access_token(identity=user, expires_delta=expires)
        return jsonify({"access_token": access_token}), 200
    return jsonify({"error": "Invalid credentials"}), 401

@bp.get('/posts')
def search_posts():
    posts = Post.query.all()
    return jsonify({'posts': [post.to_dict() for post in posts]}), 200

@bp.get('/posts/<id>')
def get_post(id):
    post = Post.query.get(id)
    return jsonify({'post': post.to_dict()}), 200

@bp.post('/posts')
@jwt_required()
def create_post():
    user = current_user
    post = Post()
    post.from_dict(request.json)
    post.user = user
    db.session.add(post)
    db.session.commit()
    return jsonify({"post": post.to_dict()}), 201

@bp.put('/posts/<id>')
@jwt_required()
def update_post(id):
    post = Post.query.get(id)
    user = current_user
    if post.user_id == user.id:
        post.from_dict(request.json)
        db.session.commit()
        return jsonify({"post": post.to_dict()}), 201
    return jsonify({"error": "There was an error!"}), 400

@bp.delete('/posts/<id>')
@jwt_required()
def delete_post(id):
    post = Post.query.get(id)
    user = current_user
    if post.user_id == user.id:
        db.session.delete(post)
        db.session.commit()
        return jsonify({"message": "Your post has been deleted successfully"}), 200
    return jsonify({"error": "There was an error!"}), 400