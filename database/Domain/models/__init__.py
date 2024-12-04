from sqlalchemy.orm import configure_mappers

from .Category import Category
from .Channel import Channel
from .DiscordUser import DiscordUser
from .Guild import Guild
from .GuildDiscordUserMapping import GuildDiscordUserMapping
from .WebsiteRole import WebsiteRole
from .WebsiteRoleUserMapping import WebsiteRoleUserMapping
from .WebsiteUser import WebsiteUser
# noinspection PyUnresolvedReferences
from ..BaseClass import Base

configure_mappers()
