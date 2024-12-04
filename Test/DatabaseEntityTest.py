from dotenv import load_dotenv

from database.Domain.WebsiteRole.Entity.WebsiteRoleUserMapping import WebsiteRoleUserMapping

load_dotenv()

from sqlalchemy import select

from src.Database.DatabaseConnection import getSession

print(getSession().scalars(select(WebsiteRoleUserMapping)).all())
