from src_backend.Routes.API.Guild.GuildDiscordUserMapping import guildDiscordUserMappingBp
from src_backend.Routes.Miscellaneous.Healthcheck import healthcheckBp
from src_backend.Routes.API.Statistic.Statistic import statisticBp
from src_backend.Routes.Auth.Auth import authBp
from src_backend.Routes.API.Guild.Guilds import guildBp
from src_backend.Routes.API.DiscordUser.DiscordUser import discordUserBp
from src_backend.Routes.API.WebsiteUser.WebsiteUser import websiteUserBp


def registerRoutes(app):
    """
    Register all routes with the main application instance.
    """
    app.register_blueprint(authBp, url_prefix="/auth")

    app.register_blueprint(discordUserBp, url_prefix="/api/discordUser")

    app.register_blueprint(guildBp, url_prefix="/api/guild")
    app.register_blueprint(guildDiscordUserMappingBp, url_prefix="/api/guildDiscordUserMapping")

    app.register_blueprint(websiteUserBp, url_prefix="/api/websiteUser")

    app.register_blueprint(statisticBp, url_prefix="/api/statistic")

    app.register_blueprint(healthcheckBp, url_prefix="/api")
