from flask import Flask
from flask_wtf import CSRFProtect
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from flask_jwt_extended import JWTManager
from flask_smorest import Api
from flask_marshmallow import Marshmallow

from config import Config

csrf = CSRFProtect()
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
http_auth = HTTPBasicAuth()
jwt = JWTManager()
smorest_api = Api()
ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    jwt.init_app(app)
    smorest_api.init_app(app)
    ma.init_app(app)

    with app.app_context():
        from app.auth import bp as auth_bp
        from app.admin import bp as admin_bp
        from app.views import bp as views_bp
        from app.api import bp as api_bp
        from app.posts_jwt import bp as posts_jwt_bp
        from app.posts_api import bp as posts_api_bp

        app.register_blueprint(auth_bp)
        app.register_blueprint(admin_bp, url_prefix='/admin')
        app.register_blueprint(views_bp)
        app.register_blueprint(api_bp, url_prefix='/api')
        app.register_blueprint(posts_jwt_bp, url_prefix='/jwt/api')
        app.register_blueprint(posts_api_bp, url_prefix='/sm/api')

        csrf.exempt(api_bp)
        csrf.exempt(posts_jwt_bp)
        csrf.exempt(posts_api_bp)
    return app