import random
import unittest
from itertools import product

from flask_jwt_extended import create_access_token
from sqlalchemy import select, func, GenerativeSelect

from database.Domain import DiscordUser
from database.Domain.models import WebsiteUser, Guild, GuildDiscordUserMapping
from src_backend import createApp
from src_backend import database


class DiscordUserApiTest(unittest.TestCase):

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

            def getQuery(sortBy: str | None = None,
                         sortOrder: str | None = None,
                         offset: int | None = None,
                         limit: int | None = None,
                         invalidTest: bool = False, ) -> tuple[GenerativeSelect | None, dict[str, str] | None]:
                """
                This function generates a query for all discord users in a guild.

                :param sortBy: The column to sort by
                :param sortOrder: The order to sort by
                :param offset: The offset to start from
                :param limit: The limit of the number of results
                :param invalidTest: If True, the test will be invalid, and we don't need the query
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
                    if sortObject:
                        sortingOrder = sortObject.asc() if sortOrder == "asc" else sortObject.desc()
                    else:
                        sortingOrder = func.rand()

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
                ) if not invalidTest else None, queryParameter

            def runMyTest(query: GenerativeSelect,
                          queryParameter: dict[str, str] | None = None,
                          invalidTest: bool = False, ):
                """
                This function runs the test for the given query and query parameters.

                :param query: The query to run
                :param queryParameter: The query parameters to use for the backend
                :param invalidTest: If True, the test will be invalid,
                                    and we don't need to run the query
                """
                response = self.client.get(f'/api/discordUser/all/{guild.guild_id}', query_string=queryParameter)

                if invalidTest:
                    self.assertTrue(400 == response.status_code or 404 == response.status_code)

                    return

                discordUsers: list[DiscordUser] = (
                    self.session
                    .execute(query)
                    .scalars()
                    .all()
                )

                self.assertEqual(200, response.status_code)
                self.assertEqual(len(discordUsers), len(response.json["discordUsers"]))

                if queryParameter:
                    # if one of the query parameters is None, we don't want to check the order
                    if not queryParameter.get("sortBy", None) or not queryParameter.get("sortOrder", None):
                        for user in discordUsers:
                            self.assertIn(user.to_dict(), response.json["discordUsers"])
                    else:
                        self.assertListEqual([user.to_dict() for user in discordUsers], response.json["discordUsers"])
                else:
                    for user in discordUsers:
                        self.assertIn(user.to_dict(), response.json["discordUsers"])

            """valid tests"""
            sortBy = [None, "discord_id", "global_name", "created_at"]
            sortOrder = [None, "asc", "desc"]
            maxCombinations = random.randint(1, 2)
            counts = [
                (start := (random.randint(0, userCount - 1)), random.randint(start, userCount),)
                for _ in range(maxCombinations)
            ]

            for sortBy, sortOrder, counts in product(sortBy, sortOrder, counts):
                offset, limit = counts

                with self.subTest(sortBy=sortBy, sortOrder=sortOrder, offset=offset, limit=limit):
                    runMyTest(*getQuery(sortBy, sortOrder))

            """invalid tests"""
            sortBy = ["invalid", 123, -123, ]
            sortOrder = ["invalid", 123, -123, ]
            counts = [
                (-1, -1),
                (0, 0),
                (userCount, userCount),
                (userCount + 1, userCount + 1),
                ("invalid", "invalid"),
            ]

            for sortBy, sortOrder, counts in product(sortBy, sortOrder, counts):
                offset, limit = counts

                with self.subTest(sortBy=sortBy, sortOrder=sortOrder, offset=offset, limit=limit):
                    runMyTest(*getQuery(sortBy, sortOrder, offset, limit, invalidTest=True), invalidTest=True)
