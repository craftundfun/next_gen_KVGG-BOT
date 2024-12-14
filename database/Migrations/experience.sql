USE kvgg_next_beta;

DROP TABLE IF EXISTS experience_boost_mapping;
DROP TABLE IF EXISTS experience;
DROP TABLE IF EXISTS xp_amount;
DROP TABLE IF EXISTS experience_amount;

CREATE TABLE IF NOT EXISTS experience (
	discord_id BIGINT UNSIGNED NOT NULL,
	guild_id   BIGINT UNSIGNED NOT NULL,
	xp         BIGINT UNSIGNED NOT NULL DEFAULT 0,

	PRIMARY KEY (discord_id, guild_id),
	FOREIGN KEY (discord_id) REFERENCES discord_user(discord_id) ON DELETE CASCADE,
	FOREIGN KEY (guild_id) REFERENCES guild(guild_id) ON DELETE CASCADE
)
	ENGINE = InnoDB
	CHARSET = UTF8MB4;

CREATE INDEX idc_discord_guild_id ON experience(discord_id, guild_id);

CREATE TABLE IF NOT EXISTS boost (
	boost_id    BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
	name        VARCHAR(255)    NOT NULL,
	description TEXT            NOT NULL,
	amount      BIGINT UNSIGNED NOT NULL DEFAULT 0,
	duration    BIGINT UNSIGNED NOT NULL DEFAULT 0,

	PRIMARY KEY (boost_id)
)
	ENGINE = InnoDB
	CHARSET = UTF8MB4;

CREATE TABLE IF NOT EXISTS experience_boost_mapping (
	id             BIGINT UNSIGNED                     NOT NULL AUTO_INCREMENT,
	boost_id       BIGINT UNSIGNED                     NOT NULL,
	discord_id     BIGINT UNSIGNED                     NOT NULL,
	guild_id       BIGINT UNSIGNED                     NOT NULL,
	remaining_time BIGINT UNSIGNED                     NOT NULL,
	created_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,

	PRIMARY KEY (id),
	FOREIGN KEY (boost_id) REFERENCES boost(boost_id) ON DELETE CASCADE,
	FOREIGN KEY (discord_id) REFERENCES discord_user(discord_id) ON DELETE CASCADE,
	FOREIGN KEY (guild_id) REFERENCES guild(guild_id) ON DELETE CASCADE
)
	ENGINE = InnoDB
	CHARSET = UTF8MB4;

CREATE INDEX idc_discord_guild_id_boost_id ON experience_boost_mapping(discord_id, guild_id, boost_id);

CREATE TABLE IF NOT EXISTS experience_amount (
	id     BIGINT UNSIGNED                                 NOT NULL AUTO_INCREMENT,
	type   ENUM ('online', 'stream', 'message', 'command') NOT NULL UNIQUE,
	amount BIGINT UNSIGNED                                 NOT NULL,

	PRIMARY KEY (id)
)
	ENGINE = InnoDB
	CHARSET = UTF8MB4;
