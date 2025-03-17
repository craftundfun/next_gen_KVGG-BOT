from datetime import datetime, date

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from database.Domain.models import Statistic
from src_backend import database
from src_backend.Logging.Logger import Logger
from src_backend.RBACCheck import hasUserMinimumRequiredRole
from src_backend.Types.Role import Role

statisticBp = Blueprint('statistic', __name__)
logger = Logger(__name__)


@statisticBp.route('/statistic/<guild_id>/<discord_id>/<date>')
@jwt_required()
@hasUserMinimumRequiredRole(Role.USER)
def getStatisticsFromUserPerGuildPerDate(guild_id, discord_id, date):
    try:
        guildId = int(guild_id)
        discordId = int(discord_id)
        date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        logger.debug(f"Invalid discord {discord_id} or guild {guild_id} id")

        return jsonify(message="Invalid discord or guild id"), 400

    selectQuery = (
        select(Statistic).where(
            Statistic.discord_id == discordId,
            Statistic.guild_id == guildId,
            Statistic.date == date,
        )
    )

    try:
        statistics: Statistic | None = database.session.execute(selectQuery).scalars().one_or_none()
    except Exception as error:
        logger.error(f"Failed to fetch statistics for user {discord_id} in guild {guildId}", exc_info=error)

        return jsonify(message="Failed to fetch statistics"), 500
    else:
        logger.debug(f"Fetched statistics for user {discordId} in guild {guildId}")

    if statistics:
        return jsonify(statistics.to_dict()), 200
    else:
        return jsonify(message="No statistics available"), 204


@statisticBp.route('/statistic/<guild_id>/<discord_id>/dates')
@jwt_required()
@hasUserMinimumRequiredRole(Role.USER)
def getAllDatesFromUserPerGuild(guild_id, discord_id):
    try:
        guildId = int(guild_id)
        discordId = int(discord_id)
    except ValueError:
        logger.debug(f"Invalid discord {discord_id} or guild {guild_id} id")

        return jsonify(message="Invalid discord or guild id"), 400

    selectQuery = (
        select(Statistic.date).where(
            Statistic.discord_id == discordId,
            Statistic.guild_id == guildId,
        )
    )

    try:
        statistics: list[date] = database.session.execute(selectQuery).scalars().all()
    except NoResultFound:
        logger.debug(f"No statistics found for user {discord_id} in guild {guildId}")

        return jsonify(message="No dates available"), 204
    except Exception as error:
        logger.error(f"Failed to fetch statistics for user {discord_id} in guild {guildId}", exc_info=error)

        return jsonify(message="Failed to fetch statistics"), 500
    else:
        logger.debug(f"Fetched statistics for user {discordId} in guild {guildId}")

    return jsonify([statistic.isoformat() for statistic in statistics]), 200
