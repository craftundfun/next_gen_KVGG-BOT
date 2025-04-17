import random
import unittest

from flask_jwt_extended import create_access_token
from sqlalchemy import select, func, GenerativeSelect

from database.Domain import DiscordUser
from database.Domain.models import WebsiteUser, Guild, GuildDiscordUserMapping
from src_backend import createApp
from src_backend import database


class BasicTests(unittest.TestCase):

    def setUp(self):
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

    def testGetAllDiscordUsers(self):
        response = self.client.get('/api/discordUser/all', )

        self.assertEqual(200, response.status_code)

        with self.app.app_context():
            # test with random order
            selectQuery = select(DiscordUser).order_by(func.rand())
            users = self.session.execute(selectQuery).scalars().all()

            userDict = {"user":
                [
                    user.to_dict() for user in users
                ]
            }

            self.assertCountEqual(userDict["user"], response.json["user"])

            for discordUser in userDict["user"]:
                self.assertIn(discordUser, response.json["user"])

    def testGetAllDiscordUsersForGuild(self):
        with self.app.app_context():
            # fetch random guild for testing
            selectQuery = select(Guild).order_by(func.rand()).limit(1)
            guild: Guild = self.session.execute(selectQuery).scalars().one()

            response = self.client.get(f'/api/discordUser/all/{guild.guild_id}')

            self.assertEqual(200, response.status_code)

            userCount = response.json["count"]

            def getQuery(sortBy: str | None,
                         sortOrder: str | None,
                         offset: int | None = None,
                         limit: int | None = None, ):
                """
                This function generates a query for all discord users in a guild.

                :param sortBy: The column to sort by
                :param sortOrder: The order to sort by
                :param offset: The offset to start from
                :param limit: The limit of the number of results
                """
                match sortBy:
                    case "discord_id":
                        sortObject = DiscordUser.discord_id
                    case "global_name":
                        sortObject = DiscordUser.global_name
                    case "created_at":
                        sortObject = DiscordUser.created_at
                    case _:
                        sortObject = None

                if sortOrder not in ["asc", "desc"]:
                    sortingOrder = func.rand()
                else:
                    sortingOrder = sortObject.asc() if sortOrder == "asc" else sortObject.desc()

                queryParameter = {}

                if sortBy:
                    queryParameter["sortBy"] = sortBy

                if sortOrder:
                    queryParameter["orderBy"] = sortOrder

                if offset:
                    queryParameter["start"] = offset

                if limit:
                    queryParameter["count"] = limit

                return (
                    select(DiscordUser)
                    .join(GuildDiscordUserMapping)
                    .where(
                        GuildDiscordUserMapping.guild_id == guild.guild_id,
                    )
                    .order_by(sortingOrder)
                    .offset(offset)
                    .limit(limit)
                ), queryParameter

            def runMyTest(query: GenerativeSelect, queryParameter: dict[str, str] | None = None):
                """
                This function runs the test for the given query and query parameters.

                :param query: The query to run
                :param queryParameter: The query parameters to use for the backend
                """
                if queryParameter:
                    response = self.client.get(f'/api/discordUser/all/{guild.guild_id}', query_string=queryParameter)
                else:
                    response = self.client.get(f'/api/discordUser/all/{guild.guild_id}')

                discordUsers: list[DiscordUser] = (
                    self.session
                    .execute(query)
                    .scalars()
                    .all()
                )

                self.assertEqual(200, response.status_code)
                self.assertEqual(len(discordUsers), len(response.json["discordUsers"]))

                if queryParameter:
                    self.assertListEqual([user.to_dict() for user in discordUsers], response.json["discordUsers"])
                else:
                    for user in discordUsers:
                        self.assertIn(user.to_dict(), response.json["discordUsers"])

            # test with random order
            runMyTest(*getQuery(sortBy=None, sortOrder=None))

            # test with discord_id asc
            runMyTest(*getQuery(sortBy="discord_id", sortOrder="asc"))

            # test with discord_id desc
            runMyTest(*getQuery(sortBy="discord_id", sortOrder="desc"))

            # test with global_name asc
            runMyTest(*getQuery(sortBy="global_name", sortOrder="asc"))

            # test with global_name desc
            runMyTest(*getQuery(sortBy="global_name", sortOrder="desc"))

            # test with created_at asc
            runMyTest(*getQuery(sortBy="created_at", sortOrder="asc"))

            # test with created_at desc
            runMyTest(*getQuery(sortBy="created_at", sortOrder="desc"))

            # test with invalid sortBy
            response = self.client.get(f'/api/discordUser/all/{guild.guild_id}?sortBy=invalid')
            self.assertEqual(400, response.status_code)

            # test with invalid orderBy
            response = self.client.get(f'/api/discordUser/all/{guild.guild_id}?orderBy=invalid')
            self.assertEqual(400, response.status_code)

            # test with invalid guild id
            response = self.client.get('/api/discordUser/all/invalid')
            self.assertEqual(400, response.status_code)

            # test with invalid start
            response = self.client.get(f'/api/discordUser/all/{guild.guild_id}?start=invalid')
            self.assertEqual(400, response.status_code)

            # test with invalid count
            response = self.client.get(f'/api/discordUser/all/{guild.guild_id}?count=invalid')
            self.assertEqual(400, response.status_code)

            # test with random offset and limit
            offset = random.randint(0, userCount - 1)
            limit = random.randint(1, userCount - offset)

            runMyTest(*getQuery(sortBy=None, sortOrder=None, offset=offset, limit=limit))
