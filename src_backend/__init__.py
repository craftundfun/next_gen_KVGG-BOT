import pymysql
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from src_backend.Config import Config
from src_backend.Extensions import database
from src_backend.Routes import registerRoutes

pymysql.install_as_MySQLdb()


def createApp():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialisiere die Datenbank und JWT
    database.init_app(app)
    JWTManager(app)

    # CORS anpassen
    cors_options = {
        "origins": "http://localhost:3000",  # Erlaubt nur das Frontend von localhost:3000
        "methods": ["GET", "POST", "PUT", "DELETE"],  # Erlaubte HTTP-Methoden
        "allow_headers": ["Content-Type", "Authorization"],  # Erlaubte Header
        "supports_credentials": True,  # Unterstützung für Cookies und Anmeldeinformationen
    }
    CORS(app, **cors_options)

    # Registriere die Routen
    registerRoutes(app)

    return app
