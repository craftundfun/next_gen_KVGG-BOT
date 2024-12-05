from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import select

from database.Domain.models.DiscordUser import DiscordUser
from src_backend import db
from src_backend.RBACCheck import hasUserMinimumRequiredRole
from src_backend.Types.Role import Role

userBp = Blueprint('user', __name__)


@userBp.route('/discordUser/all')
@jwt_required()
@hasUserMinimumRequiredRole(Role.ADMINISTRATOR)
def get_all_users():
    """
    Fetch all users from the database.
    """
    selectQuery = select(DiscordUser)
    users = db.session.execute(selectQuery).scalars().all()

    userDict: dict = {"user":
        [
            {
                "discord_id": user.discord_id,
                "profile_picture": user.profile_picture
            }
            for user in users
        ]
    }

    return jsonify(userDict)
