from src_backend.Routes.auth import authBp
from src_backend.Routes.guilds import guildBp
from src_backend.Routes.users import userBp


def registerRoutes(app):
    """
    Register all routes with the main application instance.
    """
    app.register_blueprint(authBp, url_prefix="/auth")
    app.register_blueprint(userBp, url_prefix="/api")
    app.register_blueprint(guildBp, url_prefix="/api")
