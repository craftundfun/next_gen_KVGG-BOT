USE kvgg_next_beta;

DROP TABLE IF EXISTS guild_discord_user_mapping;

CREATE TABLE IF NOT EXISTS guild (
	guild_id  BIGINT UNSIGNED UNIQUE NOT NULL,
	name      VARCHAR(255)           NOT NULL,
	joined_at DATETIME(6)            NOT NULL DEFAULT (UTC_TIMESTAMP(6)),
	icon      TEXT                            DEFAULT NULL,

	PRIMARY KEY (guild_id)
)
	ENGINE = InnoDB
	CHARSET = UTF8MB4;

CREATE TABLE IF NOT EXISTS guild_discord_user_mapping (
	guild_id        BIGINT UNSIGNED NOT NULL,
	discord_id      BIGINT UNSIGNED NOT NULL,
	display_name    VARCHAR(255)    NOT NULL,
	profile_picture TEXT            NULL DEFAULT NULL,
	joined_at       DATETIME(6)     NOT NULL,
	left_at         DATETIME(6)     NULL DEFAULT (UTC_TIMESTAMP(6)),

	PRIMARY KEY (guild_id, discord_id),
	FOREIGN KEY (guild_id) REFERENCES guild(guild_id),
	FOREIGN KEY (discord_id) REFERENCES discord_user(discord_id)
)
	ENGINE = InnoDB
	CHARSET = UTF8MB4;

# create index the other way around because the order is important
CREATE INDEX idc_discord_guild_id ON guild_discord_user_mapping(discord_id, guild_id);