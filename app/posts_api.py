from flask_smorest import Blueprint
from flask.views import MethodView
from flask import request, jsonify
from flask_jwt_extended import jwt_required, current_user

from app.models.post import Post
from app.models.user import User
from app import db

bp = Blueprint("posts_api_bp", __name__)

@bp.route('/posts')
class PostList(MethodView):
    def get(self):
        posts = Post.query.all()
        return ({'posts': [post.to_dict() for post in posts]}), 200

    @jwt_required()
    def post(self):
        user = current_user
        post = Post()
        post.from_dict(request.json)
        post.user = user
        db.session.add(post)
        db.session.commit()
        return jsonify({"post": post.to_dict()}), 201


@bp.route('/posts/<id>')
class PostDetail(MethodView):
    def get(self, id):
        post = Post.query.get(id)
        return jsonify({'post': post.to_dict()}), 200

    @jwt_required()
    def update(self, id):
        post = Post.query.get(id)
        user = current_user
        if post.user_id == user.id:
            post.from_dict(request.json)
            db.session.commit()
            return jsonify({"post": post.to_dict()}), 201
        return jsonify({"error": "There was an error!"}), 400

    @jwt_required()
    def delete(self, id):
        post = Post.query.get(id)
        user = current_user
        if post.user_id == user.id:
            db.session.delete(post)
            db.session.commit()
            return jsonify({"message": "Your post has been deleted successfully"}), 200
        return jsonify({"error": "There was an error!"}), 400