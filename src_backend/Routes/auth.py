import requests
from flask import Blueprint, jsonify, redirect, request
from flask_jwt_extended import create_access_token
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from database.Domain.models import DiscordUser
from src_backend import Config, db

authBp = Blueprint('auth', __name__)


@authBp.route('/discord')
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
        "client_id": Config.CLIENT_ID,
        "client_secret": Config.CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": f"{Config.FRONTEND_URL}/login"
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
        print("User not found")
        # TODO dont reroute to the frontend, let the frontend handle the error
        return redirect("http://localhost:3000/forbidden")
    except Exception as error:
        return jsonify(message=f"Something went wrong! {error}")

    accessToken = create_access_token(identity=str(user['id']))
    response = jsonify(message="Successfully authenticated!")
    response.headers["Authorization"] = f"Bearer {accessToken}"

    print(response.headers)

    return response
