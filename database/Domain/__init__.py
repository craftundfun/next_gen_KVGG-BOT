from sqlalchemy.orm import configure_mappers

from .models.Activity import Activity
from .models.ActivityHistory import ActivityHistory
from .models.ActivityMapping import ActivityMapping
from .models.ActivityStatistic import ActivityStatistic
from .models.BackendAccess import BackendAccess
from .models.Category import Category
from .models.Channel import Channel
from .models.ChannelSetting import ChannelSetting
from .models.DiscordUser import DiscordUser
from .models.Event import Event
from .models.Experience import Experience
from .models.ExperienceAmount import ExperienceAmount
from .models.ExperienceBoostMapping import ExperienceBoostMapping
from .models.Guild import Guild
from .models.GuildDiscordUserMapping import GuildDiscordUserMapping
from .models.History import History
from .models.Statistic import Statistic
from .models.StatusStatistic import StatusStatistic
from .models.WebsiteRole import WebsiteRole
from .models.WebsiteRoleUserMapping import WebsiteRoleUserMapping
from .models.WebsiteUser import WebsiteUser

configure_mappers()
