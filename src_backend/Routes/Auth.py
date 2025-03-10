from datetime import timedelta

import requests
from flask import Blueprint, jsonify, request, make_response
from flask_jwt_extended import create_access_token, create_refresh_token
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from database.Domain.models import DiscordUser, WebsiteUser, WebsiteRoleUserMapping
from src_backend import Config, database
from src_backend.Logging.Logger import Logger

authBp = Blueprint('auth', __name__)
# TODO own .env for backend
logger = Logger(__name__)


@authBp.route('/remindMeLogin')
def remindMeLogin():
    # print(request.cookies)
    # print("Hallo")

    return jsonify("Guten Tag", request.cookies), 200


@authBp.route('/discord')
def discordOAuth():
    """
    This function is used to authenticate the user with discord.

    :return:
    """
    code = request.args.get("code")
    remindMe = request.args.get("remindMe")

    if code is None:
        logger.error("No code was provided by Discord")

        return jsonify(message="No code was provided by Discord"), 403

    if remindMe is not None:
        remindMe = remindMe.lower() == "true"
    else:
        remindMe = False

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
        discordUser = database.session.execute(selectQuery).scalars().one()
    except NoResultFound:
        logger.warning(f"{user['username'], user['id']} not found in the database!")

        return jsonify(message="User not found in the database!"), 403
    except Exception as error:
        logger.error(f"Failed to get user {user['username'], user['id']} from the database", exc_info=error)

        return jsonify(message=f"Something went wrong!"), 500

    if not _createNecessaryThings(discordUser, user):
        return jsonify("Failed to create WebsiteUser"), 500

    accessToken = create_access_token(identity=str(user['id']))

    if remindMe:
        refreshToken = create_refresh_token(identity=str(user['id']), expires_delta=timedelta(days=14))

        try:
            selectQuery = select(WebsiteUser).where(WebsiteUser.discord_id == user['id'])
            websiteUser = database.session.execute(selectQuery).scalars().one()

            websiteUser.refresh_token = refreshToken
            database.session.commit()
        except Exception as error:
            logger.error(f"Failed to store refresh token for {user['username'], user['id']}", exc_info=error)
            database.session.rollback()

            return jsonify(message="Failed to store refresh token"), 500
    else:
        refreshToken = None

    # to build a response with a header
    response = make_response(jsonify(message="Successfully authenticated!"))

    response.headers["Authorization"] = f"Bearer {accessToken}"
    response.headers["DiscordId"] = user['id']

    # set the refresh token as a cookie
    if refreshToken:
        response.set_cookie(
            "refresh_token",
            refreshToken,
            httponly=True,
            # TODO secure für samesite=None => HTTPS lokal
            secure=False,
            samesite="None",
            max_age=int(timedelta(days=14).total_seconds()),
        )

    logger.debug(f"User {user['username'], user['id']} authenticated")

    return response, 200


# TODO better name?
def _createNecessaryThings(discordUser: DiscordUser, user: dict) -> bool:
    """
    Create WebsiteUser if it doesn't exist for the DiscordUser.

    :param discordUser: DiscordUser object
    :param user: Discord user dictionary
    :return: True if WebsiteUser was created, False otherwise
    """
    selectQuery = (select(WebsiteUser).where(WebsiteUser.discord_id == discordUser.discord_id))

    try:
        database.session.execute(selectQuery).scalars().one()
    except NoResultFound:
        websiteUser = WebsiteUser(
            discord_id=discordUser.discord_id,
            email=user['email'],
        )
        # TODO default to User, but ask database for that
        website_role_user_mapping = WebsiteRoleUserMapping(
            discord_id=discordUser.discord_id,
            role_id=1,
        )

        try:
            database.session.add(websiteUser)
            database.session.add(website_role_user_mapping)
            database.session.commit()
        except Exception as error:
            logger.error(f"Failed to create WebsiteUser for {user['username'], user['id']}", exc_info=error)
            database.session.rollback()

            return False
        else:
            logger.debug(f"Created WebsiteUser for {user['username'], user['id']}")

            return True
    except Exception as error:
        logger.error(f"Failed to fetch WebsiteUser for {user['username'], user['id']}", exc_info=error)
        database.session.rollback()

        return False
    else:
        logger.debug(f"WebsiteUser for {user['username'], user['id']} already exists")

    return True
