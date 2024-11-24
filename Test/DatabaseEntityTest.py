from dotenv import load_dotenv

from database.Domain.Category.Entity.CategoryChannelMapping import CategoryChannelMapping

load_dotenv()

from sqlalchemy import select

from src.Database.DatabaseConnection import getSession

print(getSession().scalars(select(CategoryChannelMapping)).all())
