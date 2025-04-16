USE kvgg_next_beta;

DROP TABLE IF EXISTS event;
DROP TABLE IF EXISTS history;

CREATE TABLE IF NOT EXISTS event (
	id   BIGINT UNSIGNED AUTO_INCREMENT NOT NULL,
	type VARCHAR(255) UNIQUE            NOT NULL,

	PRIMARY KEY (id)
)
	ENGINE = InnoDB
	CHARSET = UTF8MB4;

CREATE TABLE IF NOT EXISTS history (
	id              BIGINT UNSIGNED AUTO_INCREMENT NOT NULL,
	discord_id      BIGINT UNSIGNED                NOT NULL,
	guild_id        BIGINT UNSIGNED                NOT NULL,
	event_id        BIGINT UNSIGNED                NOT NULL,
	time            DATETIME(6)                    NOT NULL DEFAULT (UTC_TIMESTAMP(6)),
	channel_id      BIGINT UNSIGNED                NULL     DEFAULT NULL,
	additional_info JSON                           NULL     DEFAULT NULL,

	PRIMARY KEY (id),
	FOREIGN KEY (discord_id) REFERENCES discord_user(discord_id),
	FOREIGN KEY (guild_id) REFERENCES guild(guild_id),
	FOREIGN KEY (event_id) REFERENCES event(id),
	FOREIGN KEY (channel_id) REFERENCES channel(channel_id)
)
	ENGINE = InnoDB
	CHARSET = UTF8MB4;

CREATE INDEX idc_discord_id ON history(discord_id);
CREATE INDEX idc_guild_id ON history(guild_id);
CREATE INDEX idc_discord_guild_id ON history(discord_id, guild_id);

INSERT INTO event (id, type)
VALUES (1, 'MUTE'),
	(2, 'UNMUTE'),
	(3, 'DEAF'),
	(4, 'UNDEAF'),
	(5, 'STEAM_START'),
	(6, 'STREAM_END'),
	(7, 'VOICE_JOIN'),
	(8, 'VOICE_LEAVE'),
	(9, 'VOICE_CHANGE'),
	(10, 'ACTIVITY_START'),
	(11, 'ACTIVITY_END'),
	(12, 'ONLINE_START'),
	(13, 'ONLINE_END'),
	(14, 'IDLE_START'),
	(15, 'IDLE_END'),
	(16, 'DND_START'),
	(17, 'DND_END'),
	(18, 'OFFLINE_START'),
	(19, 'OFFLINE_END');