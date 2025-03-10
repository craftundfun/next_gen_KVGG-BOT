from flask_sqlalchemy import SQLAlchemy

from database.Domain.BaseClass import Base

database = SQLAlchemy(model_class=Base)