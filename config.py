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
    OPENAPI_URL_PREFIX = environ.get("OPENAPI_URL_PREFIX", "/")
    OPENAPI_REDOC_PATH = environ.get("OPENAPI_REDOC_PATH", "/redoc")
    OPENAPI_REDOC_URL = environ.get("OPENAPI_REDOC_URL",
        "https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"
    )
    OPENAPI_SWAGGER_UI_PATH = environ.get("OPENAPI_SWAGGER_UI_PATH", "/swagger-ui")
    OPENAPI_SWAGGER_UI_URL = environ.get("OPENAPI_SWAGGER_UI_URL", "https://cdn.jsdelivr.net/npm/swagger-ui-dist/")
    OPENAPI_RAPIDOC_PATH = environ.get("OPENAPI_RAPIDOC_PATH", "/rapidoc")
    OPENAPI_RAPIDOC_URL = environ.get("OPENAPI_RAPIDOC_PATH", "https://unpkg.com/rapidoc/dist/rapidoc-min.js")
