import random
from abc import ABC
from unittest import TestCase

from flask_jwt_extended import create_access_token
from sqlalchemy import func, select

from src_backend import createApp, database
from database.Domain.models.WebsiteUser import WebsiteUser


class BaseTest(TestCase, ABC):

    def setUp(self):
        random.seed(42)

        self.app = createApp()
        self.app.testing = True
        self.app.config["JWT_SECRET_KEY"] = "test"

        self.client = self.app.test_client()
        self.session = database.session

        with self.app.app_context():
            # select a random website user for the cookie
            selectQuery = select(WebsiteUser).order_by(func.rand()).limit(1)
            websiteUser: WebsiteUser = self.session.execute(selectQuery).scalars().one()
            access_token = create_access_token(identity=str(websiteUser.discord_id))

            self.client.set_cookie("access_token_cookie", access_token)
