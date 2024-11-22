from dotenv import load_dotenv

from database.Domain.Channel.Entity.Channel import Channel

load_dotenv()

from sqlalchemy import select

from src.Database.DatabaseConnection import getSession

print(getSession().scalars(select(Channel)).all())
