from sqlalchemy.orm import configure_mappers

from .Category import Category
from .Channel import Channel
from .DiscordUser import DiscordUser
from .Guild import Guild
from .GuildDiscordUserMapping import GuildDiscordUserMapping
from .WebsiteRole import WebsiteRole
from .WebsiteRoleUserMapping import WebsiteRoleUserMapping
from .WebsiteUser import WebsiteUser
from .History import History
from .Event import Event
from .Statistic import Statistic
from .ChannelSetting import ChannelSetting
from .Experience import Experience
from .Boost import Boost
from .ExperienceBoostMapping import ExperienceBoostMapping
from .ExperienceAmount import ExperienceAmount
# noinspection PyUnresolvedReferences
from ..BaseClass import Base

configure_mappers()
