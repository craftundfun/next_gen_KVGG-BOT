from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from database.Domain.models import Guild
from src_backend import database
from src_backend.Logging.Logger import Logger
from src_backend.RBACCheck import hasUserMinimumRequiredRole
from src_backend.Types.Role import Role

guildBp = Blueprint('guild', __name__)
logger = Logger(__name__)


@guildBp.route('/all')
@jwt_required()
@hasUserMinimumRequiredRole(Role.USER)
def getAllGuilds():
    """
    Fetch all guilds from the database.
    """
    selectQuery = (select(Guild))

    try:
        guilds: list[Guild] = database.session.execute(selectQuery).scalars().all()
    except Exception as error:
        logger.error("Failed to fetch all guilds", exc_info=error)

        return jsonify({"message": "Failed to fetch all guilds"}), 500

    logger.debug("Fetched all guilds")

    return jsonify({'guilds': [guild.to_dict() for guild in guilds]}), 200


@guildBp.route('/<guild_id>')
@jwt_required()
@hasUserMinimumRequiredRole(Role.USER)
def getGuild(guild_id):
    try:
        guildId = int(guild_id)
    except ValueError:
        logger.debug(f"Invalid guild id {guild_id}")

        return jsonify(message="Invalid guild id"), 400

    if guildId < 0:
        logger.warning(f"Invalid guild id {guildId}")

        return jsonify(message="Invalid guild id"), 400

    selectQuery = (select(Guild).where(Guild.guild_id == guildId))

    try:
        guild: Guild = database.session.execute(selectQuery).scalars().one()
    except NoResultFound:
        logger.debug(f"No guild found with id {guildId}")

        return jsonify(message="Guild does not exist"), 404
    except Exception as error:
        logger.error(f"Failed to fetch guild with id {guildId}", exc_info=error)

        return jsonify(message="Failed to fetch guild"), 500
    else:
        logger.debug(f"Fetched guild with id {guildId}")

        return jsonify(guild.to_dict()), 200


@guildBp.route('/mine')
@jwt_required()
@hasUserMinimumRequiredRole(Role.USER)
def getMyFavouriteGuild():
    userId = get_jwt_identity()

    if not userId:
        return jsonify("UserId from token not present"), 404

    selectQuery = (select(Guild).order_by(Guild.guild_id.asc()).limit(1))

    try:
        guild: Guild = database.session.execute(selectQuery).scalars().one()
    except Exception as error:
        logger.error(f"Failed to fetch guild", exc_info=error)

        return jsonify(message="Failed to fetch guild"), 500
    else:
        logger.debug(f"Fetched guild with id {guild.guild_id}")

        return jsonify(guild.to_dict()), 200
