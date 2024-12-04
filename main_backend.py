# important
import os
from datetime import timedelta

import pymysql
import requests
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from database.Domain.BaseClass import Base
from database.Domain.DiscordUser.Entity.DiscordUser import DiscordUser

pymysql.install_as_MySQLdb()
from flask import Flask, jsonify, request, redirect
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app,
     supports_credentials=True,
     resources={r"*": {"origins": "*"}},
     allow_headers=["Authorization", "Content-Type"], )

db = SQLAlchemy(model_class=Base)
app.config['SQLALCHEMY_DATABASE_URI'] = (f'mysql://{os.getenv("DATABASE_USER")}:{os.getenv("DATABASE_PASSWORD")}'
                                         f'@{os.getenv("DATABASE_HOST")}/{os.getenv("DATABASE_NAME")}')
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")  #
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=15)
jwt = JWTManager(app)
db.init_app(app)


@app.route('/auth/discord')
def discordOAuth():
    """
    This function is used to authenticate the user with discord.

    :return:
    """
    code = request.args.get("code")

    if code is None:
        return jsonify(message="Something went wrong!")

    # url to get the access token
    url = "https://discord.com/api/oauth2/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "client_id": os.getenv("CLIENT_ID"),
        "client_secret": os.getenv("CLIENT_SECRET"),
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://127.0.0.1:3000/login"
    }

    response = requests.post(url, headers=headers, data=data)

    try:
        response.raise_for_status()
    except Exception as error:
        return jsonify(message=f"Something went wrong! {error}")

    # authorization header
    headers = {
        "Authorization": f"{response.json()['token_type']} {response.json()['access_token']}",
    }
    response = requests.get("https://discord.com/api/users/@me", headers=headers)

    try:
        response.raise_for_status()
    except Exception as error:
        return jsonify(message=f"Something went wrong! {error}")

    user: dict = response.json()
    selectQuery = (select(DiscordUser).where(DiscordUser.discord_id == user['id']))

    try:
        db.session.execute(selectQuery).scalars().one()
    except NoResultFound:
        # TODO dont reroute to the frontend, let the frontend handle the error
        return redirect("http://localhost:3000/forbidden")
    except Exception as error:
        return jsonify(message=f"Something went wrong! {error}")

    accessToken = create_access_token(identity=str(user['id']))
    response = jsonify(message="Successfully authenticated!")
    response.headers["Authorization"] = f"Bearer {accessToken}"

    return response


@app.route("/api/discordUser/all")
@jwt_required()
def getUser():
    """
    This function is used to get all the users from the database.

    :return:
    """
    selectQuery = select(DiscordUser)
    users = db.session.execute(selectQuery).scalars().all()

    userDict: dict = {"user": [{"discord_id": user.discord_id} for user in users]}

    return jsonify(userDict)


@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = 'http://127.0.0.1:3000'
    response.headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'
    response.headers['Access-Control-Expose-Headers'] = 'Authorization'
    response.headers['Access-Control-Allow-Credentials'] = 'true'

    return response


if __name__ == '__main__':
    app.run(debug=not bool(int(os.getenv("PRODUCTION"))), host='0.0.0.0', port=8000)
