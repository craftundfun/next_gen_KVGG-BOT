from dotenv import load_dotenv

from database.Domain.models.WebsiteRoleUserMapping import WebsiteRoleUserMapping

load_dotenv()

from sqlalchemy import select

from src_bot.Database.DatabaseConnection import getSession

print(getSession().scalars(select(WebsiteRoleUserMapping)).all()[0].website_role.role_name)
