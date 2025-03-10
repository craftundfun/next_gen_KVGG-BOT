from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import select

from database.Domain.models import Guild
from src_backend import database
from src_backend.Logging.Logger import Logger
from src_backend.RBACCheck import hasUserMinimumRequiredRole
from src_backend.Types.Role import Role

guildBp = Blueprint('guild', __name__)
logger = Logger(__name__)


@guildBp.route('/guild/all')
@jwt_required()
@hasUserMinimumRequiredRole(Role.ADMINISTRATOR)
def getAllGuilds():
    """
    Fetch all guilds from the database.
    """
    logger.debug(f"{get_jwt_identity()} is fetching all guilds")

    selectQuery = (select(Guild))

    try:
        guilds = database.session.execute(selectQuery).scalars().all()
    except Exception as error:
        logger.error("Failed to fetch all guilds", exc_info=error)

        return jsonify({"message": "Failed to fetch all guilds"}), 500

    # Convert the guilds to a list of dictionaries, iterate over each column to avoid sqlalchemy metadata
    guildList: list = [{column.name: getattr(guild, column.name) for column in guild.__table__.columns}
                       for guild in guilds]

    logger.debug("Fetched all guilds")

    return jsonify({'guilds': guildList}), 200
