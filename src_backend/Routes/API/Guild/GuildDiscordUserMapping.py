from src_backend.Logging.Logger import Logger

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from database.Domain.models import GuildDiscordUserMapping
from src_backend import database
from src_backend.RBACCheck import hasUserMinimumRequiredRole
from src_backend.Types.Role import Role

guildDiscordUserMappingBp = Blueprint('guildDiscordUserMapping', __name__)
logger = Logger(__name__)


@guildDiscordUserMappingBp.route('/<guild_id>/<discord_id>')
@jwt_required()
@hasUserMinimumRequiredRole(Role.USER)
def getMapping(guild_id, discord_id):
    try:
        guildId = int(guild_id)
        discordId = int(discord_id)
    except ValueError:
        logger.debug(f"Invalid guild id {guild_id} or discord id {discord_id}")

        return jsonify(message="Invalid guild id or discord id"), 400

    if guildId < 0 or discordId < 0:
        logger.warning(f"Invalid guild id {guildId} or discord id {discordId}")

        return jsonify(message="Invalid guild id or discord id"), 400

    selectQuery = (
        select(GuildDiscordUserMapping).where(
            GuildDiscordUserMapping.guild_id == guildId,
            GuildDiscordUserMapping.discord_id == discordId,
        )
    )

    try:
        mapping: GuildDiscordUserMapping = database.session.execute(selectQuery).scalars().one()
    except NoResultFound:
        logger.debug(f"No mapping found for guild id {guildId} and discord id {discordId}")

        return jsonify(message="Mapping does not exist"), 404
    except Exception as error:
        logger.error(f"Failed to fetch mapping with guild id {guildId} and discord id {discordId}", exc_info=error)

        return jsonify(message="Failed to fetch mapping"), 500

    return jsonify(mapping.to_dict()), 200
