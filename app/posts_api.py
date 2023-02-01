from flask_smorest import Blueprint
from flask.views import MethodView
from flask import request, jsonify
from flask_jwt_extended import jwt_required, current_user

from app.models.post import Post
from app.models.user import User
from app.schemas.post import post_schema, posts_schema, post_schema_update
from app import db

bp = Blueprint("posts_api_bp", __name__)

@bp.route('/posts')
class PostList(MethodView):
    @bp.response(200, posts_schema)
    def get(self):
        posts = Post.query.all()
        # return ({'posts': [post.to_dict() for post in posts]}), 200
        return posts

    @bp.arguments(post_schema)
    @bp.response(201, post_schema)
    @jwt_required()
    def post(self, post):
        # user = current_user
        # post = Post()
        # post.from_dict(request.json)
        # post.user = user
        # db.session.add(post)
        # db.session.commit()
        # return jsonify({"post": post.to_dict()}), 201
        post.user = current_user
        db.session.add(post)
        db.session.commit()
        return post


@bp.route('/posts/<id>')
class PostDetail(MethodView):
    @bp.response(200, post_schema)
    def get(self, id):
        """Find posts

        Return posts.
        ---
        Internal comment not meant to be exposed.
        """

        post = Post.query.get(id)
        # return jsonify({'post': post.to_dict()}), 200
        return post

    @bp.arguments(post_schema_update)
    @bp.response(200, post_schema)
    @jwt_required()
    def put(self, data, id):
        post = Post.query.get(id)
        if post.user_id == current_user.id:
            post.body = data.get('body')
            db.session.commit()
        return post

    @jwt_required()
    def delete(self, id):
        post = Post.query.get(id)
        user = current_user
        if post.user_id == user.id:
            db.session.delete(post)
            db.session.commit()
            return jsonify({"message": "Your post has been deleted successfully"}), 200
        return jsonify({"error": "There was an error!"}), 400