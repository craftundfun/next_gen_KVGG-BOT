from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from database.Domain.models.DiscordUser import DiscordUser
from src_backend import database
from src_backend.Logging.Logger import Logger
from src_backend.RBACCheck import hasUserMinimumRequiredRole
from src_backend.Types.Role import Role

discordUserBp = Blueprint('discordUser', __name__)
logger = Logger(__name__)


@discordUserBp.route("/all")
@jwt_required()
@hasUserMinimumRequiredRole(Role.ADMINISTRATOR)
def getAllDiscordUsers():
    """
    Fetch all users from the database.
    """
    selectQuery = select(DiscordUser)
    users = database.session.execute(selectQuery).scalars().all()

    userDict: dict = {"user":
        [
            user.to_dict() for user in users
        ]
    }

    return jsonify(userDict)


@discordUserBp.route('/<discord_id>')
@jwt_required()
@hasUserMinimumRequiredRole(Role.USER)
def getDiscordUser(discord_id):
    """
    Fetches a specific DiscordUser by its discord_id from the database.

    :param discord_id: Discord ID of the user
    """
    try:
        discord_id = int(discord_id)
    except ValueError:
        return jsonify(message="Invalid discord id"), 400

    selectQuery = select(DiscordUser).where(DiscordUser.discord_id == discord_id)

    try:
        discordUser: DiscordUser = database.session.execute(selectQuery).scalars().one()
    except NoResultFound:
        return jsonify(message="DiscordUser does not exist"), 404
    except Exception as error:
        logger.error(f"Failed to fetch DiscordUser with ID: {discord_id}", exc_info=error)

        return jsonify(message="Failed to fetch DiscordUser"), 500

    return jsonify(discordUser.to_dict()), 200


@discordUserBp.route("/me")
@jwt_required()
@hasUserMinimumRequiredRole(Role.USER)
def getMe():
    userId = get_jwt_identity()

    if not userId:
        return jsonify("UserId from token not present"), 404

    selectQuery = select(DiscordUser).where(DiscordUser.discord_id == int(userId))

    try:
        discordUser: DiscordUser = database.session.execute(selectQuery).scalars().one()
    except NoResultFound:
        logger.warning(f"No DiscordUser found with the provided discord_id: {userId}")

        return jsonify(message="DiscordUser does not exist"), 404
    except Exception as error:
        logger.error(f"Failed to get DiscordUser from the database for discord_id: {userId}", exc_info=error)

        return jsonify(message="Something went wrong!"), 500

    return jsonify(discordUser.to_dict()), 200
