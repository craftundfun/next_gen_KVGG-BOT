from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from database.Domain.models.DiscordUser import DiscordUser
from src_backend import db
from src_backend.Logging.Logger import Logger
from src_backend.RBACCheck import hasUserMinimumRequiredRole
from src_backend.Types.Role import Role

userBp = Blueprint('user', __name__)
logger = Logger(__name__)


@userBp.route('/discordUser/all')
@jwt_required()
@hasUserMinimumRequiredRole(Role.ADMINISTRATOR)
def getAllDiscordUsers():
    """
    Fetch all users from the database.
    """
    selectQuery = select(DiscordUser)
    users = db.session.execute(selectQuery).scalars().all()

    userDict: dict = {"user":
        [
            user.to_dict() for user in users
        ]
    }

    return jsonify(userDict)

@userBp.route('/discordUser/<discord_id>')
@jwt_required()
@hasUserMinimumRequiredRole(Role.ADMINISTRATOR)
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
        discordUser: DiscordUser = db.session.execute(selectQuery).scalars().one()
    except NoResultFound:
        return jsonify(message="DiscordUser does not exist"), 404
    except Exception as error:
        logger.error(f"Failed to fetch DiscordUser with ID: {discord_id}", exc_info=error)

        return jsonify(message="Failed to fetch DiscordUser"), 500

    return jsonify(discordUser.to_dict())
