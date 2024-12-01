# important
import os

import pymysql
import requests
from flask_sqlalchemy import SQLAlchemy

from database.Domain.BaseClass import Base

pymysql.install_as_MySQLdb()
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)
db = SQLAlchemy(model_class=Base)
app.config['SQLALCHEMY_DATABASE_URI'] = (f'mysql://{os.getenv("DATABASE_USER")}:{os.getenv("DATABASE_PASSWORD")}'
                                         f'@{os.getenv("DATABASE_HOST")}/{os.getenv("DATABASE_NAME")}')

db.init_app(app)


@app.route('/api/hello')
def hello_world():
    return jsonify(message="Hello from Bjarne! :)")


@app.route('/auth/discord')
def test():
    code = request.args.get("code")

    if code is None:
        return jsonify(message="Code is missing"), 400

    url = "https://discord.com/api/oauth2/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "client_id": os.getenv("CLIENT_ID"),
        "client_secret": os.getenv("CLIENT_SECRET"),
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://127.0.0.1:8000/auth/discord"
    }
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()

    headers = {
        "Authorization": f"{response.json()['token_type']} {response.json()['access_token']}",
    }
    response = requests.get("https://discord.com/api/users/@me", headers=headers)
    response.raise_for_status()

    return jsonify(response.json())


if __name__ == '__main__':
    app.run(debug=not bool(int(os.getenv("PRODUCTION"))), host='0.0.0.0', port=8000)
