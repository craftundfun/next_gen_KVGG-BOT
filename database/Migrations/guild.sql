USE kvgg_next_beta;

DROP TABLE IF EXISTS guild;

CREATE TABLE IF NOT EXISTS guild (
	guild_id  BIGINT UNSIGNED UNIQUE NOT NULL,
	name      VARCHAR(255)           NOT NULL,
	joined_at DATETIME(6)            NOT NULL DEFAULT (UTC_TIMESTAMP(6)),
	icon      TEXT                            DEFAULT NULL,

	PRIMARY KEY (guild_id)
)
	ENGINE = InnoDB
	CHARSET = UTF8MB4;

DROP TABLE IF EXISTS guild_discord_user_mapping;

# maybe we don't need this table, but we will see
CREATE TABLE IF NOT EXISTS guild_discord_user_mapping (
	guild_id        BIGINT UNSIGNED NOT NULL,
	discord_user_id BIGINT UNSIGNED NOT NULL,
	display_name    VARCHAR(255)    NOT NULL,
	left_at         DATETIME(6)     NULL DEFAULT (UTC_TIMESTAMP(6)),

	PRIMARY KEY (guild_id, discord_user_id),
	FOREIGN KEY (guild_id) REFERENCES guild(guild_id),
	FOREIGN KEY (discord_user_id) REFERENCES discord_user(discord_id)
)
	ENGINE = InnoDB
	CHARSET = UTF8MB4;

CREATE INDEX idc_discord_guild_id ON guild_discord_user_mapping(discord_user_id, guild_id);