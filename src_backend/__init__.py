import pymysql
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from src_backend.Config import Config
from src_backend.Extensions import db
from src_backend.Routes import registerRoutes

pymysql.install_as_MySQLdb()


def createApp():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    JWTManager(app)
    CORS(app,
         supports_credentials=True,
         resources={r"*": {"origins": "*"}},
         allow_headers=["Authorization", "Content-Type"], )

    registerRoutes(app)

    return app



