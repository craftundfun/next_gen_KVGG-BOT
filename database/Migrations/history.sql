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
	# at the moment we dont need the history longer than for the time calculation, so we can safely delete it
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

INSERT INTO event (type)
VALUES ('MUTE'),
	('UNMUTE'),
	('DEAF'),
	('UNDEAF'),
	('STEAM_START'),
	('STREAM_END'),
	#('WEBCAM_START'),
	#('WEBCAM_END'),
	('VOICE_JOIN'),
	('VOICE_LEAVE'),
	('VOICE_CHANGE'),
	('ACTIVITY START'),
	('ACTIVITY END');