from itertools import product

from sqlalchemy import select, func

from database.Domain.models.GuildDiscordUserMapping import GuildDiscordUserMapping
from src_backend.Tests.API.BaseTest import BaseTest


class GuildDiscordMappingApiTest(BaseTest):
    def testGetMapping(self):
        with self.app.app_context():
            # fetch random guild and discord user for testing
            selectQuery = select(GuildDiscordUserMapping).order_by(func.rand()).limit(1)
            mapping: GuildDiscordUserMapping = self.session.execute(selectQuery).scalars().one()

            response = self.client.get(f'/api/guildDiscordUserMapping/{mapping.guild_id}/{mapping.discord_id}')

            self.assertEqual(200, response.status_code)

            mappingDict = mapping.to_dict()

            self.assertEqual(mappingDict, response.json)

            discordIds = [-1, "invalid"]
            guildIds = [-1, "invalid"]

            for discordId, guildId in product(discordIds, guildIds):
                with self.subTest(discordIds=discordIds, guildIds=guildIds):
                    response = self.client.get(f'/api/guildDiscordUserMapping/{guildId}/{discordId}')
                    self.assertEqual(400, response.status_code)

            response = self.client.get(f'/api/guildDiscordUserMapping/{mapping.guild_id}/123')
            self.assertEqual(404, response.status_code)

            response = self.client.get(f'/api/guildDiscordUserMapping/123/{mapping.discord_id}')
            self.assertEqual(404, response.status_code)

            response = self.client.get(f'/api/guildDiscordUserMapping/123/123')
            self.assertEqual(404, response.status_code)
