from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import select, func
from sqlalchemy.exc import NoResultFound

from database.Domain.models import GuildDiscordUserMapping
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

    return jsonify(userDict), 200


@discordUserBp.route("/all/<guild_id>")
@jwt_required()
@hasUserMinimumRequiredRole(Role.USER)
def getAllDiscordUsersForGuild(guild_id):
    try:
        guildId = int(guild_id)
    except ValueError:
        return jsonify(message="Invalid guild id"), 400

    start = int(request.args.get("start", 0))
    count = int(request.args.get("count", 9999999))
    sortBy = request.args.get("sortBy", "discord_id")
    sortOrder = request.args.get("orderBy", "asc")

    match sortBy:
        case "discord_id":
            sortObject = DiscordUser.discord_id
        case "global_name":
            sortObject = DiscordUser.global_name
        case "created_at":
            sortObject = DiscordUser.created_at
        case _:
            # just in case
            logger.warning(f"Invalid sortBy parameter: {sortBy}")

            return jsonify(message="Invalid sortBy parameter"), 400

    selectQuery = (
        select(DiscordUser)
        .join(GuildDiscordUserMapping)
        .where(GuildDiscordUserMapping.guild_id == guildId, )
        .offset(start)
        .limit(count)
        .order_by(
            sortObject.asc() if sortOrder == "asc" else sortObject.desc()
        )
    )

    try:
        discordUsers: list[DiscordUser] = database.session.execute(selectQuery).scalars().all()
    except NoResultFound:
        logger.warning(f"No DiscordUser found for the provided guild_id: {guildId}")

        return jsonify(message="DiscordUser does not exist"), 404
    except Exception as error:
        logger.error(f"Failed to fetch DiscordUser for guild_id: {guildId}", exc_info=error)

        return jsonify(message="Something went wrong!"), 500

    selectQuery = (
        select(func.count())
        .select_from(DiscordUser)
        .join(GuildDiscordUserMapping)
        .where(GuildDiscordUserMapping.guild_id == guildId)
    )

    try:
        discordUsersCount: int = database.session.execute(selectQuery).scalars().one()
    except Exception as error:
        logger.error(f"Failed to fetch DiscordUser count for guild_id: {guildId}", exc_info=error)

        return jsonify(message="Something went wrong!"), 500

    return jsonify({"count": discordUsersCount, "discordUsers": [user.to_dict() for user in discordUsers]}), 200


@discordUserBp.route("/all/<guild_id>/count")
@jwt_required()
@hasUserMinimumRequiredRole(Role.USER)
def getDiscordUsersCountForGuild(guild_id):
    """
    Count all Discord users for a specific guild.
    """
    try:
        guildId = int(guild_id)
    except ValueError:
        return jsonify(message="Invalid guild id"), 400

    selectQuery = (
        select(func.count())
        .select_from(DiscordUser)
        .join(GuildDiscordUserMapping)
        .where(GuildDiscordUserMapping.guild_id == guildId)
    )

    print("Test")

    try:
        discordUsersCount: int = database.session.execute(selectQuery).scalars().one()
    except Exception as error:
        logger.error(f"Failed to fetch DiscordUser count for guild_id: {guildId}", exc_info=error)

        return jsonify(message="Something went wrong!"), 500

    return jsonify({"count": discordUsersCount}), 200


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
