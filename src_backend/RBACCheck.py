from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from sqlalchemy import select

from database.Domain.models import WebsiteRoleUserMapping, WebsiteRole
from src_backend import db
from src_backend.Logging.Logger import Logger
from src_backend.Types.Role import Role

logger = Logger(__name__)


def hasUserSpecificRoles(*roles: Role):
    """
    Check if the user has the required roles to access the endpoint

    :param roles: Names of the roles that are required to access the endpoint
    :return:
    """

    def inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            userId = get_jwt_identity()

            if not userId:
                logger.warning("Unauthorized: Missing user id")

                return jsonify(message="Unauthorized: Missing user id"), 401

            selectQuery = (
                select(WebsiteRoleUserMapping)
                .where(WebsiteRoleUserMapping.discord_id == userId, )
            )

            try:
                websiteRoleUserMapping = db.session.execute(selectQuery).scalars().all()
                websiteRoleUserMapping: [WebsiteRoleUserMapping] = list(websiteRoleUserMapping)
            except Exception as error:
                logger.error(f"Couldn't fetch websiteRoleUserMapping for user {userId}", exc_info=error)

                return jsonify(message=f"Something went wrong! {error}")

            currentUserRoles = [mapping.website_role.role_name for mapping in websiteRoleUserMapping]

            # check if the user has one of the required roles
            if not any(role.value in currentUserRoles for role in roles):
                logger.warning(f"Forbidden: Insufficient permissions. User {userId} has roles {currentUserRoles}")

                return jsonify(message="Forbidden: Insufficient permissions"), 403

            logger.debug(f"User {userId} can access the endpoint")

            return func(*args, **kwargs)

        return wrapper

    return inner


def hasUserMinimumRequiredRole(role: Role):
    def inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            userId = get_jwt_identity()

            if not userId:
                logger.warning("Unauthorized: Missing user id")

                return jsonify(message="Unauthorized: Missing user id"), 401

            selectQueryRolesOfUser = (
                select(WebsiteRoleUserMapping)
                .join(WebsiteRole)
                .where(WebsiteRoleUserMapping.discord_id == userId, )
                .order_by(WebsiteRole.priority.desc())
                .limit(1)
            )
            selectQueryWebsiteRole = (
                select(WebsiteRole)
                .where(WebsiteRole.role_name == role.value, )
            )

            try:
                websiteRoleUserMapping = db.session.execute(selectQueryRolesOfUser).scalars().one()
                minimumRequiredRole = db.session.execute(selectQueryWebsiteRole).scalars().one()
            except Exception as error:
                logger.error(f"Couldn't fetch websiteRoleUserMapping for user {userId}", exc_info=error)

                return jsonify(message=f"Something went wrong! {error}"), 500

            # the highest priority of the user is not enough
            if websiteRoleUserMapping.website_role.priority < minimumRequiredRole.priority:
                logger.warning(f"Forbidden: Insufficient permissions. "
                               f"User {userId} has role {websiteRoleUserMapping.website_role.role_name}")

                return jsonify(message="Forbidden: Insufficient permissions"), 403

            return func(*args, **kwargs)

        return wrapper

    return inner
