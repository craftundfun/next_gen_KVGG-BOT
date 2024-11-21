from dotenv import load_dotenv

load_dotenv()

from sqlalchemy import select

from database.Domain.Channel.Entity.ChannelGuildMapping import ChannelGuildMapping
from src.Database.DatabaseConnection import getSession

print(getSession().scalars(select(ChannelGuildMapping)).all())
