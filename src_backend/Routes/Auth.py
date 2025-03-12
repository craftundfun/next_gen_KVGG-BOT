from datetime import timedelta

import requests
from flask import Blueprint, jsonify, request, make_response, redirect
from flask_jwt_extended import create_access_token, create_refresh_token
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from database.Domain.models import DiscordUser, WebsiteUser, WebsiteRoleUserMapping
from src_backend import Config, database
from src_backend.Logging.Logger import Logger

authBp = Blueprint('auth', __name__)
# TODO own .env for backend
logger = Logger(__name__)


@authBp.route('/login')
def login():
    """
    The frontend calls this upon loading the website.
    If the user has a refresh token, he gets an access token and the necessary information is returned.
    """
    if not request.cookies:
        logger.debug("No cookies were provided, redirecting to Discord OAuth")

        return jsonify("No cookies were provided"), 400

    if not (refreshToken := request.cookies.get("refresh_token")):
        logger.debug("No refresh token was provided, redirecting to Discord OAuth")

        return jsonify("No refresh token was provided"), 400

    selectQueryWebsiteUser = (select(WebsiteUser).where(WebsiteUser.refresh_token == refreshToken))

    try:
        websiteUser: WebsiteUser = database.session.execute(selectQueryWebsiteUser).scalars().one()
    except NoResultFound:
        logger.debug("No WebsiteUser found with the provided refresh token, redirecting to Discord OAuth")

        return jsonify("No WebsiteUser found with the provided refresh token"), 400
    except Exception as error:
        logger.error("Failed to get WebsiteUser from the database", exc_info=error)

        return jsonify(message="Something went wrong!"), 500

    selectQueryDiscordUser = (select(DiscordUser).where(DiscordUser.discord_id == websiteUser.discord_id))

    try:
        discordUser: DiscordUser = database.session.execute(selectQueryDiscordUser).scalars().one()
    except NoResultFound:
        logger.debug("No DiscordUser found with the provided discord id")

        return jsonify(message="No DiscordUser found with the provided discord id"), 400
    except Exception as error:
        logger.error("Failed to get DiscordUser from the database", exc_info=error)

        return jsonify(message="Something went wrong!"), 500

    accessToken = create_access_token(identity=str(discordUser.discord_id))

    response = make_response(jsonify("Successfully logged in!"))
    response.headers["Authorization"] = f"Bearer {accessToken}"
    response.headers["DiscordUser"] = discordUser.to_dict()
    response.headers["WebsiteUser"] = websiteUser.to_dict()

    return response, 200


@authBp.route('/newLogin')
def newLogin():
    code = request.args.get("code")

    if code is None:
        logger.error("No code was provided by Discord")

        return jsonify(message="No code was provided by Discord"), 500

    refreshToken = request.args.get("remindMe", None)

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
        "redirect_uri": f"{Config.URL}/login"
    }

    response = requests.post(url, headers=headers, data=data)

    try:
        response.raise_for_status()
    except Exception as error:
        logger.error("Failed to get access token", exc_info=error)

        return jsonify(message="Something went wrong!"), 500

    # get information from discord about the user
    headers = {
        "Authorization": f"{response.json()['token_type']} {response.json()['access_token']}",
    }
    response = requests.get("https://discord.com/api/users/@me", headers=headers)

    try:
        response.raise_for_status()
    except Exception as error:
        logger.error("Failed to get user information", exc_info=error)

        return jsonify(message="Something went wrong!"), 500

    user: dict = response.json()
    selectQueryDiscordUser = (select(DiscordUser).where(DiscordUser.discord_id == user['id']))

    try:
        discordUser = database.session.execute(selectQueryDiscordUser).scalars().one()
    except NoResultFound:
        logger.warning(f"{user['username'], user['id']} not found in the database!")

        return jsonify(message="User not found in the database!"), 403
    except Exception as error:
        logger.error(f"Failed to get user {user['username'], user['id']} from the database", exc_info=error)

        return jsonify(message="Something went wrong!"), 500

    if not (websiteUser := _createNecessaryThings(discordUser, user)):
        return jsonify("Failed to create WebsiteUser"), 500

    response = make_response(jsonify("Successfully authenticated!"))
    accessToken = create_access_token(identity=str(discordUser.discord_id))

    if refreshToken:
        refreshToken = create_refresh_token(identity=str(discordUser.discord_id), expires_delta=timedelta(days=14))

        try:
            websiteUser.refresh_token = refreshToken
            database.session.commit()
        except Exception as error:
            # if this fails, just ignore it
            logger.error(f"Failed to store refresh token for {user['username'], user['id']}", exc_info=error)
            database.session.rollback()
        else:
            response.set_cookie(
                "refresh_token",
                refreshToken,
                httponly=True,
                secure=True,
                samesite="Strict",
                max_age=int(timedelta(days=14).total_seconds()),
            )

    response.headers["Authorization"] = f"Bearer {accessToken}"
    response.headers["DiscordUser"] = discordUser.to_dict()
    response.headers["WebsiteUser"] = websiteUser.to_dict()

    return response, 200


@authBp.route('/remindMeLogin')
def remindMeLogin():
    if not request.cookies:
        logger.debug("No cookies were provided")

        return jsonify(message="No cookies were provided"), 403

    selectQuery = (select(WebsiteUser).where(WebsiteUser.refresh_token == request.cookies.get("refresh_token")))

    try:
        websiteUser = database.session.execute(selectQuery).scalars().one()
    except NoResultFound:
        logger.debug("No WebsiteUser found with the provided refresh token")

        return jsonify(message="No WebsiteUser found with the provided refresh token"), 403
    except Exception as error:
        logger.error("Failed to get WebsiteUser from the database", exc_info=error)

        return jsonify(message="Something went wrong!"), 500

    accessToken = create_access_token(identity=str(websiteUser.discord_id))

    response = make_response(jsonify(message="Successfully reauthenticated!"))
    response.headers["Authorization"] = f"Bearer {accessToken}"
    response.headers["DiscordId"] = websiteUser.discord_id

    return response, 200


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
