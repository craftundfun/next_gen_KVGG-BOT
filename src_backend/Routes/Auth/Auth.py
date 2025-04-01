from datetime import timedelta
from urllib.parse import parse_qs

import requests
from flask import Blueprint, jsonify, request, make_response, redirect
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from database.Domain.models import DiscordUser, WebsiteUser, WebsiteRoleUserMapping
from src_backend import Config, database
from src_backend.Logging.Logger import Logger

authBp = Blueprint('auth', __name__)
# TODO own .env for backend
logger = Logger(__name__)


@authBp.route('/loginCallback')
def loginCallback():
    """
    Discord OAuth callback.
    """
    code = request.args.get("code")
    state = request.args.get("state")
    params = parse_qs(state)
    remindMe = params.get("remindMe", ["false"])[0] == "true"

    if code is None:
        logger.error("Discord OAuth code was not provided")

        return jsonify("Discord OAuth code was not provided"), 500

    url = "https://discord.com/api/oauth2/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "client_id": Config.CLIENT_ID,
        "client_secret": Config.CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": f"{Config.URL}/api/loginCallback",
    }

    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
    except Exception as error:
        logger.error("Failed to get access token from Discord", exc_info=error)

        return jsonify(message="Something went wrong!"), 500

    if response.status_code != 200:
        logger.error("Something went wrong with the Discord OAuth process", exc_info=response.json())

        return jsonify(message="Something went wrong!"), 500

    # get information from discord about the user
    headers = {
        "Authorization": f"{response.json()['token_type']} {response.json()['access_token']}",
    }

    try:
        response = requests.get("https://discord.com/api/users/@me", headers=headers)
        response.raise_for_status()
    except Exception as error:
        logger.error("Failed to get user information", exc_info=error)

        return jsonify(message="Something went wrong!"), 500

    if response.status_code != 200:
        logger.error("Something went wrong with the data request from Discord", exc_info=response.json())

        return jsonify(message="Something went wrong!"), 500

    user: dict = response.json()
    logger.debug(f"User information received from Discord: {user}")

    if not (websiteUser := doesUserExist(user)):
        return redirect(Config.URL + "/forbidden", code=302)

    response = redirect(Config.URL + "/dashboard", code=302)

    if remindMe:
        refreshToken = create_refresh_token(identity=str(user['id']), expires_delta=timedelta(days=14))
        response.set_cookie(
            "refresh_token_cookie",
            refreshToken,
            httponly=True,
            secure=True,
            samesite="Strict",
            max_age=int(timedelta(days=14).total_seconds()),
        )

        websiteUser.refresh_token = refreshToken

        try:
            database.session.commit()
        except Exception as error:
            logger.error(f"Failed to save refresh token for {user['username'], user['id']}", exc_info=error)
            database.session.rollback()

    accessToken = create_access_token(identity=str(user['id']))
    response.set_cookie(
        "access_token_cookie",
        accessToken,
        httponly=True,
        secure=True,
        samesite="Strict",
        max_age=int(timedelta(minutes=10).total_seconds()),
    )

    # no code because we are redirecting, otherwise it will not work
    return response


@authBp.route('/welcomeBack')
@jwt_required()
def refresh():
    """
    This will be called when the user comes back to the website. The before and after request handle everything,
    and this is just a placeholder to show that the user is logged in.
    """
    return jsonify("Hello World!"), 200


def doesUserExist(user: dict) -> WebsiteUser | None:
    selectQuery = (select(DiscordUser).where(DiscordUser.discord_id == user['id']))

    try:
        discordUser = database.session.execute(selectQuery).scalars().one()
    except NoResultFound:
        logger.warning(f"DiscordUser for {user['username'], user['id']} who tried to log in does not exist")

        return None
    except Exception as error:
        logger.error(f"Failed to fetch DiscordUser for {user['username'], user['id']}", exc_info=error)
        database.session.rollback()

        return None

    logger.debug(f"DiscordUser for {user['username'], user['id']} does exist")

    return _createNecessaryThings(discordUser, user)


# TODO better name?
def _createNecessaryThings(discordUser: DiscordUser, user: dict) -> WebsiteUser | None:
    """
    Create WebsiteUser if it doesn't exist for the DiscordUser.

    :param discordUser: DiscordUser object
    :param user: Discord user dictionary
    :return: The WebsiteUser if it was found or created, None otherwise
    """
    selectQuery = (select(WebsiteUser).where(WebsiteUser.discord_id == discordUser.discord_id))

    try:
        websiteUser = database.session.execute(selectQuery).scalars().one()
    except NoResultFound:
        logger.debug(f"WebsiteUser for {user['username'], user['id']} does not exist, creating it")

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

            return None
        else:
            logger.debug(f"Created WebsiteUser for {user['username'], user['id']}")

            return websiteUser
    except Exception as error:
        logger.error(f"Failed to fetch WebsiteUser for {user['username'], user['id']}", exc_info=error)
        database.session.rollback()

        return None
    else:
        logger.debug(f"WebsiteUser for {user['username'], user['id']} already exists")

        return websiteUser
