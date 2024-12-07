from src_backend.Routes.Auth import authBp
from src_backend.Routes.Guilds import guildBp
from src_backend.Routes.Users import userBp
from src_backend.Routes.WebsiteUsers import websiteUserBp


def registerRoutes(app):
    """
    Register all routes with the main application instance.
    """
    app.register_blueprint(authBp, url_prefix="/auth")
    app.register_blueprint(userBp, url_prefix="/api")
    app.register_blueprint(guildBp, url_prefix="/api")
    app.register_blueprint(websiteUserBp, url_prefix="/api")
