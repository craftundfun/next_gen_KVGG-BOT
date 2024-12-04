from flask_sqlalchemy import SQLAlchemy

from database.Domain.BaseClass import Base

db = SQLAlchemy(model_class=Base)