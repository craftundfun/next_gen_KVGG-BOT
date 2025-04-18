from datetime import datetime, date, timedelta
from itertools import product

from sqlalchemy import select, func

from database.Domain.models.Statistic import Statistic
from src_backend.Tests.API.BaseTest import BaseTest


class StatisticApiTest(BaseTest):
    def setUp(self):
        super().setUp()

        with self.app.app_context():
            selectQuery = select(Statistic).order_by(func.rand()).limit(1)
            self.statistic: Statistic = self.session.execute(selectQuery).scalars().one()

    def testGetStatisticsFromUserPerGuildPerDate(self):
        response = self.client.get(
            f'/api/statistic/{self.statistic.guild_id}/{self.statistic.discord_id}/{self.statistic.date}'
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual(self.statistic.to_dict(), response.json)

        invalidGuildIds = [-1, "invalid", "", 123]
        invalidDiscordIds = [-1, "invalid", "", 123]
        invalidDates = ["invalid", "", 123, "2023-01-01", "2023-01-01T00:00:00Z"]

        for guildId, discordId, date in product(invalidGuildIds, invalidDiscordIds, invalidDates):
            with self.subTest(guildId=guildId, discordId=discordId, date=date):
                # if one of the values in empty, the code should be 404
                if guildId == invalidGuildIds[2] or discordId == invalidDiscordIds[2] or date == invalidDates[1]:
                    code = 404
                # if the ids are integers and the date is a valid date, the code should be 204 -> no statistics
                elif guildId == invalidGuildIds[3] and discordId == invalidDiscordIds[3] and date == invalidDates[3]:
                    code = 204
                else:
                    code = 400

                response = self.client.get(
                    f'/api/statistic/{guildId}/{discordId}/{date}'
                )

                self.assertEqual(
                    code,
                    response.status_code,
                    msg=f"Invalid request for guildId {guildId}, discordId {discordId}, date {date}",
                )

    def testGetAllDatesFromUserPerGuild(self):
        response = self.client.get(
            f'/api/statistic/{self.statistic.guild_id}/{self.statistic.discord_id}/dates'
        )

        self.assertEqual(200, response.status_code)

        with self.app.app_context():
            selectQuery = (
                select(Statistic.date)
                .where(
                    Statistic.guild_id == self.statistic.guild_id,
                    Statistic.discord_id == self.statistic.discord_id,
                )
                .order_by(Statistic.date.asc())
            )

            statistics: list[date] = self.session.execute(selectQuery).scalars().all()

            # dates not filled up
            self.assertNotEqual([statistic.isoformat() for statistic in statistics], response.json)

            startDate = statistics[0]
            endDate = datetime.now().date()

            for days in range(1, (endDate - startDate).days + 1):
                if (startDate + timedelta(days=days)) in statistics:
                    continue

                statistics.append(startDate + timedelta(days=days))

            # dates filled up
            self.assertEqual([statistic.isoformat() for statistic in statistics], response.json)

        invalidGuildIds = [-1, "invalid", "", 123]
        invalidDiscordIds = [-1, "invalid", "", 123]

        for guildId, discordId in product(invalidGuildIds, invalidDiscordIds):
            with self.subTest(guildId=guildId, discordId=discordId):
                # if one of the values in empty, the code should be 404
                if guildId == invalidGuildIds[2] or discordId == invalidDiscordIds[2]:
                    code = 404
                # if the ids are integers, the code should be 204 -> no statistics
                elif guildId == invalidGuildIds[3] and discordId == invalidDiscordIds[3]:
                    code = 204
                else:
                    code = 400

                response = self.client.get(
                    f'/api/statistic/{guildId}/{discordId}/dates'
                )

                self.assertEqual(
                    code,
                    response.status_code,
                    msg=f"Invalid request for guildId {guildId}, discordId {discordId}",
                )

    def testFetchAllStatisticsFromUserPerGuildForPeriod(self):
        # TODO
        pass