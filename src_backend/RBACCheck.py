from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from sqlalchemy import select

from database.Domain.models import WebsiteRoleUserMapping
from src_backend import db


def hasUserSpecificRoles(*roles: str):
    def inner(func):
        @wraps(func)  # Bewahrt die Metadaten der ursprünglichen Funktion
        def wrapper(*args, **kwargs):
            userId = get_jwt_identity()

            if not userId:
                return jsonify(message="Unauthorized: Missing user id"), 401

            selectQuery = (select(WebsiteRoleUserMapping).where(WebsiteRoleUserMapping.discord_id == userId))

            try:
                websiteRoleUserMapping = db.session.execute(selectQuery).scalars().all()
                websiteRoleUserMapping: [WebsiteRoleUserMapping] = list(websiteRoleUserMapping)
            except Exception as error:
                return jsonify(message=f"Something went wrong! {error}")

            currentUserRoles = [mapping.website_role.role_name for mapping in websiteRoleUserMapping]

            # Prüfen, ob der Benutzer die erforderlichen Rollen hat
            if not any(role in currentUserRoles for role in roles):
                return jsonify(message="Forbidden: Insufficient permissions"), 403

            return func(*args, **kwargs)

        return wrapper

    return inner
