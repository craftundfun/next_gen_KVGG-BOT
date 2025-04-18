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
            response = self.client.get(f'/api/guild/{guild.guild_id}')

            self.assertEqual(200, response.status_code)

            guildDict = guild.to_dict()

            self.assertEqual(guildDict, response.json)

            response = self.client.get(f'/api/guild/{-1}')
            self.assertEqual(400, response.status_code)

            response = self.client.get(f'/api/guild/invalid')
            self.assertEqual(400, response.status_code)

    def testGetMyFavouriteGuild(self):
        # TODO implement this later, currently this function is not correctly implemented
        pass
