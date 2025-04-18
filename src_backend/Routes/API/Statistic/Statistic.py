from datetime import datetime, date, timedelta

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


@statisticBp.route('/<guild_id>/<discord_id>/<date>')
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

    if guildId < 0 or discordId < 0:
        logger.warning(f"Invalid discord {discord_id} or guild {guild_id} id")

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


@statisticBp.route('/<guild_id>/<discord_id>/dates')
@jwt_required()
@hasUserMinimumRequiredRole(Role.USER)
def getAllDatesFromUserPerGuild(guild_id, discord_id):
    """
    Returns all dates for a user in a guild. Fills missing dates with empty statistics.
    """
    try:
        guildId = int(guild_id)
        discordId = int(discord_id)
    except ValueError:
        logger.debug(f"Invalid discord {discord_id} or guild {guild_id} id")

        return jsonify(message="Invalid discord or guild id"), 400

    if guildId < 0 or discordId < 0:
        logger.warning(f"Invalid discord {discord_id} or guild {guild_id} id")

        return jsonify(message="Invalid discord or guild id"), 400

    selectQuery = (
        select(Statistic.date)
        .where(
            Statistic.discord_id == discordId,
            Statistic.guild_id == guildId,
        )
        .order_by(Statistic.date.asc())
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

    if not statistics:
        return jsonify(message="No dates available"), 204

    # add "missing" dates to the list
    startDate = statistics[0]
    endDate = datetime.now().date()

    for days in range(1, (endDate - startDate).days + 1):
        if (startDate + timedelta(days=days)) in statistics:
            continue

        statistics.append(startDate + timedelta(days=days))

    return jsonify([statistic.isoformat() for statistic in statistics]), 200


@statisticBp.route('/<guild_id>/<discord_id>/<start_date>/<end_date>')
@jwt_required()
@hasUserMinimumRequiredRole(Role.USER)
def fetchStatisticsFromUserPerGuildForPeriod(guild_id, discord_id, start_date, end_date):
    """
    Fetches all statistics from a user in a guild for a given period.
    Empty days are included in the response.

    :param guild_id: The ID of the guild
    :param discord_id: The ID of the user
    :param start_date: The start date of the period (YYYY-MM-DD)
    :param end_date: The end date of the period (YYYY-MM-DD)
    """
    try:
        guildId = int(guild_id)
        discordId = int(discord_id)
        startDate = datetime.strptime(start_date, "%Y-%m-%d").date()
        endDate = datetime.strptime(end_date, "%Y-%m-%d").date()
    except ValueError:
        logger.debug(f"Invalid parameters given")

        return jsonify(message="Invalid parameters given"), 400

    selectQuery = (
        select(Statistic).where(
            Statistic.discord_id == discordId,
            Statistic.guild_id == guildId,
            Statistic.date.between(startDate, endDate),
        )
    )

    try:
        statistics: list[Statistic] = database.session.execute(selectQuery).scalars().all()
    except NoResultFound:
        logger.debug(f"No statistics found for user {discord_id} in guild {guildId} "
                     f"for period {start_date} to {end_date}")

        return jsonify(message="No statistics available"), 204
    except Exception as error:
        logger.error(f"Failed to fetch statistics for user {discord_id} in guild {guildId}", exc_info=error)

        return jsonify(message="Failed to fetch statistics"), 500
    else:
        logger.debug(f"Fetched statistics for user {discordId} in guild {guildId} "
                     f"for period {start_date} to {end_date}")

    earliestDate = min(statistic.date for statistic in statistics)
    latestDate = max(statistic.date for statistic in statistics)

    # include day with no data to have a consecutive list
    for i in range(1, (latestDate - earliestDate).days):
        if (earliestDate + timedelta(days=i)) in list(statistic.date for statistic in statistics):
            continue

        statistics.append(
            Statistic(
                discord_id=discordId,
                guild_id=guildId,
                date=earliestDate + timedelta(days=i),
            )
        )

    statistics.sort(key=lambda statistic: statistic.date)
    return jsonify([statistic.to_dict() for statistic in statistics]), 200
