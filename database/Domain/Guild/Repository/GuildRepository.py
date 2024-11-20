from discord import Guild as DiscordGuild
from sqlalchemy import select
from sqlalchemy.exc import MultipleResultsFound, NoResultFound
from sqlalchemy.orm import Session

from database.Domain.Guild.Entity.Guild import Guild
from src.Logging.Logger import Logger

logger = Logger("GuildRepository")


class GuildRepository:

    def __init__(self, session: Session):
        self.session = session

    def getGuild(self, guild: DiscordGuild) -> Guild | None:
        """
        Fetch a guild from the database if it doesn't exist call to create it

        :param guild: Discord guild to fetch
        :return:
        """
        selectQuery = select(Guild).where(Guild.guild_id == guild.id)

        with self.session:
            try:
                databaseGuild = self.session.scalars(selectQuery).one()
            except MultipleResultsFound:
                logger.error(f"Found multiple guilds with id: {guild.id}")

                return None
            except NoResultFound:
                logger.debug(f"No guild found with id: {guild.id}")

                return self._createGuild(guild)
            except Exception as error:
                logger.error(f"Failed to get guild: {error}", exc_info=error)

                return None
            else:
                return databaseGuild

    def _createGuild(self, guild: DiscordGuild) -> Guild | None:
        """
        Create a guild in the database

        :param guild: Guild to create
        :return: DatabaseGuild if successful, None otherwise
        """
        databaseGuild = Guild(
            guild_id=guild.id,
            name=guild.name,
        )

        try:
            self.session.add(databaseGuild)
            self.session.commit()
        except Exception as error:
            logger.error(f"Failed to create guild: {error}", exc_info=error)

            return None

        return databaseGuild
