from flask import Blueprint, jsonify
from src_backend import database
from database.Domain.models import Statistic
from src_backend.Logging.Logger import Logger
from flask_jwt_extended import jwt_required
from src_backend.RBACCheck import hasUserMinimumRequiredRole
from src_backend.Types.Role import Role
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

statisticBp = Blueprint('statistic', __name__)
logger = Logger(__name__)


@statisticBp.route('/statistic/<guild_id>/<discord_id>')
@jwt_required()
@hasUserMinimumRequiredRole(Role.USER)
# TODO fetch with correct date etc.
def getStatisticsFromUserPerGuild(guild_id, discord_id):
    try:
        guildId = int(guild_id)
        discordId = int(discord_id)
    except ValueError:
        logger.debug(f"Invalid discord {discord_id} or guild {guild_id} id")

        return jsonify(message="Invalid discord or guild id"), 400

    selectQuery = (
        select(Statistic).where(
            Statistic.discord_id == discordId,
            Statistic.guild_id == guildId,
        )
    )

    try:
        statistics: list[Statistic] = list(database.session.execute(selectQuery).scalars().all())
    except NoResultFound:
        logger.debug(f"No statistics found for user {discordId} in guild {guildId}")

        return jsonify(message="Statistics not found"), 404
    except Exception as error:
        logger.error(f"Failed to fetch statistics for user {discord_id} in guild {guildId}", exc_info=error)

        return jsonify(message="Failed to fetch statistics"), 500
    else:
        logger.debug(f"Fetched statistics for user {discordId} in guild {guildId}")

    return jsonify(statistics[0].to_dict()), 200
