from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))

class Config:
    SECRET_KEY = environ.get("SECRET_KEY", "12345")
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
    JWT_SECRET_KEY = environ.get("JWT_SECRET_KEY", "4IZ0xWtJMJOilqDl7Q")
    API_TITLE = environ.get("API_TITLE", "Silabuz miniblog")
    API_VERSION = environ.get("API_VERSION", "v1")
    OPENAPI_VERSION = environ.get("OPENAPI_VERSION", "3.0.2")