from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from database.Domain.models import WebsiteUser
from src_backend import database
from src_backend.Logging.Logger import Logger
from src_backend.RBACCheck import hasUserMinimumRequiredRole
from src_backend.Types.Role import Role

websiteUserBp = Blueprint('websiteUserBp', __name__)
logger = Logger(__name__)


@websiteUserBp.route('/<discord_id>')
@jwt_required()
@hasUserMinimumRequiredRole(Role.ADMINISTRATOR)
def getWebsiteUser(discord_id):
    try:
        discordId = int(discord_id)
    except ValueError:
        logger.debug(f"Invalid discord id: {discord_id}, type: {type(discord_id)}")

        return jsonify(message="Invalid discord id"), 400

    selectQuery = (select(WebsiteUser).where(WebsiteUser.discord_id == discordId))

    try:
        websiteUser = database.session.execute(selectQuery).scalars().one()
    except NoResultFound:
        return jsonify(message="WebsiteUser does not exist"), 404
    except Exception as error:
        logger.error(f"Failed to fetch WebsiteUser with ID: {discordId}", exc_info=error)

        return jsonify(message="Failed to fetch WebsiteUser"), 500
    else:
        logger.debug(f"Fetched WebsiteUser with ID: {discordId}")

    return jsonify(websiteUser.to_dict())


@websiteUserBp.route('/me')
@jwt_required()
@hasUserMinimumRequiredRole(Role.USER)
def getMe():
    userId = get_jwt_identity()

    if not userId:
        return jsonify("UserId from token not present"), 500

    selectQuery = select(WebsiteUser).where(WebsiteUser.discord_id == int(userId))

    try:
        websiteUser: WebsiteUser = database.session.execute(selectQuery).scalars().one()
    except NoResultFound:
        logger.warning(f"No WebsiteUser found with the provided discord_id: {userId}")

        return jsonify(message="WebsiteUser does not exist"), 404
    except Exception as error:
        logger.error(f"Failed to get WebsiteUser from the database for discord_id: {userId}", exc_info=error)

        return jsonify(message="Something went wrong!"), 500

    return jsonify(websiteUser.to_dict()), 200
