import ipaddress
from datetime import datetime, timedelta

import pymysql
import requests
import sqlalchemy.exc
from flask import Flask, jsonify, request, redirect, Response
from flask_cors import CORS
from flask_jwt_extended import JWTManager, verify_jwt_in_request, create_access_token, get_jwt_identity
from flask_jwt_extended.exceptions import NoAuthorizationError
from sqlalchemy import null
from werkzeug.middleware.proxy_fix import ProxyFix

from database.Domain.models.BackendAccess import BackendAccess
from src_backend.Config import Config
from src_backend.Extensions import database
from src_backend.Logging.Logger import Logger
from src_backend.Routes import registerRoutes

pymysql.install_as_MySQLdb()
logger = Logger(__name__)


def createApp():
    app = Flask(__name__)
    app.config.from_object(Config)

    # to allow Flask to see the real IP behind the two proxies
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=2, x_proto=1, x_host=1, x_prefix=1)

    # Initialisiere die Datenbank und JWT
    database.init_app(app)
    jwt = JWTManager(app)

    @jwt.unauthorized_loader
    def noJWTinRequest(errorFromFlask: str):
        """
        Callback when no JWT is found in the request.
        Flask-JWT-Extended will call this function
        when the user tries to access a protected route without providing a JWT.
        """
        logger.warning("No IP address found in request")

        if not request.cookies.get("access_token_cookie", None):
            return jsonify(message="No (accepted) access cookie provided!", error=errorFromFlask), 401
        else:
            return jsonify(message="No refresh token cookie provided!", error=errorFromFlask), 401

    @app.before_request
    # allow session and refresh tokens
    def before_request():
        # try to verify the JWT (access token)
        try:
            verify_jwt_in_request(refresh=False, verify_type=True)

            return
        except NoAuthorizationError:
            logger.debug("Failed to verify JWT, try to generate a new one with refresh token")

            # try to verify the refresh token (if applicable)
            try:
                verify_jwt_in_request(refresh=True, verify_type=True)
            except NoAuthorizationError:
                # we cant reverify this user, let them run into the 401
                logger.debug("Failed to verify refresh token")

                return

            logger.debug(f"JWT verification successful for userId: {get_jwt_identity()}, creating new access token")

            userId = get_jwt_identity()
            access_token = create_access_token(identity=userId)

            response = redirect(request.path)
            response.set_cookie(
                "access_token_cookie",
                access_token,
                httponly=True,
                secure=True,
                samesite="Strict",
                max_age=int(timedelta(minutes=10).total_seconds()),
            )

            return response

    @app.after_request
    def afterRequest(response: Response):
        # add CORS headers to the response
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS, PUT, DELETE"

        # we dont want to log the health check
        if request.path == "/api/health":
            return response

        forwarded_for = request.headers.get("X-Forwarded-For", "")
        ip: str | None = forwarded_for.split(",")[0].strip() if forwarded_for else request.remote_addr

        try:
            ip = str(ipaddress.ip_address(ip))
        except ValueError:
            logger.warning(f"Invalid IP address format: {ip}")

            ip = None

        if not ip:
            logger.warning("Invalid IP address format")

            return response

        countryName = None
        countryCode = None

        # for unauthorized requests, we want their geolocation
        if response.status_code == 401:
            try:
                # https://www.geojs.io/docs/v1/endpoints/country/
                url = f'https://get.geojs.io/v1/ip/country/{ip}.json'
                apiResponse = requests.get(url)

                if apiResponse.status_code == 200:
                    countryName = apiResponse.json().get('name', None)
                    countryCode = apiResponse.json().get('country', None)
                else:
                    logger.warning(f"Failed to get country code for IP {ip}")
            except Exception as error:
                logger.error("Error while getting country code", exc_info=error)

        # some responses have no data
        try:
            data = response.get_data(as_text=True)
        except AttributeError:
            data = None

        backendAccess = BackendAccess(
            ip_address=ip,
            country_code=countryCode,
            country_name=countryName,
            access_time=datetime.now(),
            authorized=response.status_code != 401,
            path=request.path,
            response_code=response.status_code,
            response=data,
            query_header=str(request.args.to_dict()) if len(request.args.to_dict().keys()) > 0 else null(),
        )

        try:
            database.session.add(backendAccess)
            database.session.commit()
        except (sqlalchemy.exc.OperationalError, pymysql.err.OperationalError) as error:
            logger.warning("Database connection error, skipping backend access save", exc_info=error)
        except Exception as error:
            logger.error("Error while saving backend access", exc_info=error)
            database.session.rollback()

        return response

    # CORS anpassen
    cors_options = {
        "origins": "http://localhost:3000",  # Erlaubt nur das Frontend von localhost:3000
        "methods": ["GET", "POST", "PUT", "DELETE"],  # Erlaubte HTTP-Methoden
        "allow_headers": ["Content-Type", "Authorization"],  # Erlaubte Header
        "supports_credentials": True,  # Unterstützung für Cookies und Anmeldeinformationen
    }

    CORS(app, **cors_options)

    registerRoutes(app)

    return app
