from typing import Any

from sqlalchemy import select, func

from database.Domain.models.Guild import Guild
from src_backend.Tests.API.BaseTest import BaseTest


class GuildApiTest(BaseTest):
    def testGetAllGuilds(self):
        response = self.client.get('/api/guild/all')

        self.assertEqual(200, response.status_code)

        with self.app.app_context():
            selectQuery = select(Guild).order_by(func.rand())
            guilds = self.session.execute(selectQuery).scalars().all()
            guildDict = {"guild":
                [
                    guild.to_dict() for guild in guilds
                ]
            }

            self.assertCountEqual(guildDict["guild"], response.json["guilds"])

            for guild in guildDict["guild"]:
                self.assertIn(guild, response.json["guilds"])

    def testGetGuild(self):
        with self.app.app_context():
            # fetch random guild for testing
            selectQuery = select(Guild).order_by(func.rand()).limit(1)
            guild: Guild = self.session.execute(selectQuery).scalars().one()
            guildDict = guild.to_dict()

            response = self.client.get(f'/api/guild/{guild.guild_id}')

            self.assertEqual(200, response.status_code)
            self.assertEqual(guildDict, response.json)

            invalidIds: list[tuple[Any, int]] = [(-1, 400), ("invalid", 400), ("", 404), (123, 404)]

            for invalidId, expectedStatusCode in invalidIds:
                with self.subTest(invalidId=invalidId, expectedStatusCode=expectedStatusCode):
                    response = self.client.get(f'/api/guild/{invalidId}')

                    self.assertEqual(
                        expectedStatusCode,
                        response.status_code,
                        msg=f"Invalid status code for ({invalidId})",
                    )

    def testGetMyFavouriteGuild(self):
        # TODO implement this later, currently this function is not correctly implemented
        pass
