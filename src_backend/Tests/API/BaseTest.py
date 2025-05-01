import atexit
import signal
import sys
from abc import ABC
from unittest import TestCase

from flask_jwt_extended import create_access_token
from testcontainers.mysql import MySqlContainer

from database.Domain import WebsiteUser
from database.Domain.BaseClass import Base
from src_backend import createApp, database
from src_backend.Tests.API.getObjects import getDiscordUsers, getGuilds, getGuildDiscordUserMappings, getWebsiteUsers, \
    getActivities, getEvents, getActivityMappings, getActivityHistory, getActivityStatistics, getChannels, \
    getChannelSettings, getBoost, getCategories, getExperiences, getHistories, getStatistics, getStatusStatistics, \
    getWebsiteRoles, getWebsiteRoleUserMappings

mysql = MySqlContainer("mysql:8.0.32")


def cleanup():
    try:
        print("Stopping MySQL container and cleaning up...")
        mysql.stop()
    except Exception as e:
        print(f"Error stopping container: {e}")
        pass


atexit.register(cleanup)

for sig in (signal.SIGINT, signal.SIGTERM):
    signal.signal(sig, lambda signum, frame: sys.exit(1))


class BaseTest(TestCase, ABC):

    @classmethod
    def setUpClass(cls):
        mysql.start()

        test_uri = mysql.get_connection_url()

        cls.app = createApp({
            "SQLALCHEMY_DATABASE_URI": test_uri,
            "TESTING": True,
            "SQLALCHEMY_ECHO": False,
            "JWT_SECRET_KEY": "test",
        })

        cls.app.testing = True
        cls.client = cls.app.test_client()

        with cls.app.app_context():
            # create cookie to access the API
            # TODO choose specific user for testing because of permissions
            cls.client.set_cookie(
                "access_token_cookie",
                create_access_token(identity=str(list(getWebsiteUsers())[0].discord_id)),
            )

    def setUp(self):
        # Fixtures pro Test
        with self.app.app_context():
            try:
                database.drop_all()
                database.create_all()

                database.session.bulk_save_objects(getDiscordUsers())
                database.session.bulk_save_objects(getGuilds())
                database.session.bulk_save_objects(getGuildDiscordUserMappings())
                database.session.bulk_save_objects(getWebsiteUsers())
                database.session.bulk_save_objects(getActivities())
                database.session.bulk_save_objects(getEvents())
                database.session.bulk_save_objects(getActivityHistory())
                database.session.bulk_save_objects(getActivityMappings())
                database.session.bulk_save_objects(getActivityStatistics())
                database.session.bulk_save_objects(getBoost())
                database.session.bulk_save_objects(getCategories())
                database.session.bulk_save_objects(getChannels())
                database.session.bulk_save_objects(getChannelSettings())
                database.session.bulk_save_objects(getExperiences())
                database.session.bulk_save_objects(getHistories())
                database.session.bulk_save_objects(getStatistics())
                database.session.bulk_save_objects(getStatusStatistics())
                database.session.bulk_save_objects(getWebsiteRoles())
                database.session.bulk_save_objects(getWebsiteRoleUserMappings())

                database.session.commit()
            except Exception as error:
                print(f"Error during setup: {error}")

                sys.exit(1)

        self.session = database.session

    def tearDown(self):
        with self.app.app_context():
            pass

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            database.session.remove()
            Base.metadata.drop_all(bind=database.engine)

        mysql.stop()
