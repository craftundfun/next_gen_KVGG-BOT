USE kvgg_next_beta;

DROP TABLE IF EXISTS statistic;
DROP TABLE IF EXISTS activity_statistic;
DROP TABLE IF EXISTS status_statistic;

CREATE TABLE IF NOT EXISTS statistic (
	discord_id    BIGINT UNSIGNED NOT NULL,
	guild_id      BIGINT UNSIGNED NOT NULL,
	date          DATE            NOT NULL,
	# Auch wenn es gegen die Datenbank-Konsistenz spricht,
	# ist es einfacher beide Foreign Keys aus DiscordID und GuildID zu nutzen.
	# Andernfalls müsste man beim einfügen immer erst joinen bzw. die passende ID suchen.
	# guild_discord_user_mapping_id BIGINT UNSIGNED                NOT NULL,

	# microseconds online due to lack of timedelta in MySQL
	online_time   BIGINT UNSIGNED NOT NULL DEFAULT 0,
	stream_time   BIGINT UNSIGNED NOT NULL DEFAULT 0,
	mute_time     BIGINT UNSIGNED NOT NULL DEFAULT 0,
	deaf_time     BIGINT UNSIGNED NOT NULL DEFAULT 0,
	message_count BIGINT UNSIGNED NOT NULL DEFAULT 0,
	command_count BIGINT UNSIGNED NOT NULL DEFAULT 0,

	PRIMARY KEY (discord_id, guild_id, date),
	FOREIGN KEY (discord_id) REFERENCES discord_user(discord_id),
	FOREIGN KEY (guild_id) REFERENCES guild(guild_id)
)
	ENGINE = InnoDB
	CHARSET = UTF8MB4;

CREATE INDEX idc_discord_guild_id ON statistic(discord_id, guild_id);
CREATE INDEX idc_discord_guild_date ON statistic(discord_id, guild_id, date);

CREATE TABLE IF NOT EXISTS activity_statistic (
	discord_id  BIGINT UNSIGNED NOT NULL,
	guild_id    BIGINT UNSIGNED NOT NULL,
	activity_id BIGINT UNSIGNED NOT NULL,
	date        DATE            NOT NULL,
	time        BIGINT UNSIGNED NOT NULL DEFAULT 0,

	PRIMARY KEY (discord_id, guild_id, activity_id, date),
	FOREIGN KEY (discord_id) REFERENCES discord_user(discord_id),
	FOREIGN KEY (guild_id) REFERENCES guild(guild_id),
	FOREIGN KEY (activity_id) REFERENCES activity(id)
)
	ENGINE = InnoDB
	CHARSET = UTF8MB4;

CREATE TABLE IF NOT EXISTS status_statistic (
	discord_id  BIGINT UNSIGNED NOT NULL,
	guild_id    BIGINT UNSIGNED NOT NULL,
	date        DATE            NOT NULL,

	# microseconds online due to lack of timedelta in MySQL
	online_time BIGINT UNSIGNED NOT NULL DEFAULT 0,
	idle_time   BIGINT UNSIGNED NOT NULL DEFAULT 0,
	dnd_time    BIGINT UNSIGNED NOT NULL DEFAULT 0,

	PRIMARY KEY (discord_id, guild_id, date)
)

	ENGINE = InnoDB
	CHARSET = UTF8MB4;

