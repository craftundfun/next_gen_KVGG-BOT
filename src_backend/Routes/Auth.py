import requests
from flask import Blueprint, jsonify, request, make_response
from flask_jwt_extended import create_access_token
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from database.Domain.models import DiscordUser
from src_backend import Config, db
from src_backend.Logging.Logger import Logger

authBp = Blueprint('auth', __name__)
# TODO own .env for backend
logger = Logger(__name__)


@authBp.route('/discord')
def discordOAuth():
    """
    This function is used to authenticate the user with discord.

    :return:
    """
    code = request.args.get("code")

    if code is None:
        logger.error("No code was provided by Discord")

        return jsonify(message="No code was provided by Discord"), 403

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
        logger.error("Failed to get access token", exc_info=error)

        return jsonify(message=f"Something went wrong!"), 403

    # authorization header
    headers = {
        "Authorization": f"{response.json()['token_type']} {response.json()['access_token']}",
    }
    response = requests.get("https://discord.com/api/users/@me", headers=headers)

    try:
        response.raise_for_status()
    except Exception as error:
        logger.error("Failed to get user information", exc_info=error)

        return jsonify(message=f"Something went wrong!"), 500

    user: dict = response.json()
    selectQuery = (select(DiscordUser).where(DiscordUser.discord_id == user['id']))

    try:
        db.session.execute(selectQuery).scalars().one()
    except NoResultFound:
        logger.warning(f"{user['username'], user['id']} not found in the database!")

        return jsonify(message="User not found in the database!"), 403
    except Exception as error:
        logger.error(f"Failed to get user {user['username'], user['id']} from the database", exc_info=error)

        return jsonify(message=f"Something went wrong!"), 500

    accessToken = create_access_token(identity=str(user['id']))
    response = make_response(jsonify(message="Successfully authenticated!"))

    response.headers["Authorization"] = f"Bearer {accessToken}"
    response.headers["DiscordId"] = user['id']

    logger.debug(f"User {user['username'], user['id']} authenticated")

    return response, 200
