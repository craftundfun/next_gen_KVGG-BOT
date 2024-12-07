USE kvgg_next_beta;

DROP TABLE IF EXISTS events;
DROP TABLE IF EXISTS history;

CREATE TABLE IF NOT EXISTS events (
	id   BIGINT UNSIGNED AUTO_INCREMENT NOT NULL,
	type VARCHAR(255)                   NOT NULL,

	PRIMARY KEY (id)
)
	ENGINE = InnoDB
	CHARSET = UTF8MB4;

CREATE TABLE IF NOT EXISTS history (
	id              BIGINT UNSIGNED AUTO_INCREMENT NOT NULL,
	discord_id      BIGINT UNSIGNED                NOT NULL,
	guild_id        BIGINT UNSIGNED                NOT NULL,
	event_id        BIGINT UNSIGNED                NOT NULL,
	time            TIMESTAMP                      NOT NULL DEFAULT CURRENT_TIMESTAMP,
	additional_info TEXT                           NULL     DEFAULT NULL,

	PRIMARY KEY (id),
	FOREIGN KEY (discord_id) REFERENCES discord_user(discord_id),
	FOREIGN KEY (guild_id) REFERENCES guild(guild_id),
	FOREIGN KEY (event_id) REFERENCES events(id)
)
	ENGINE = InnoDB
	CHARSET = UTF8MB4;

CREATE INDEX idc_discord_id ON history(discord_id);
CREATE INDEX idc_guild_id ON history(guild_id);
CREATE INDEX idc_event_id ON history(event_id);

INSERT INTO events (type)
VALUES ('MUTE'),
	('UNMUTE'),
	('STEAM_START'),
	('STREAM_END'),
	('WEBCAM_START'),
	('WEBCAM_END'),
	('VOICE_JOIN'),
	('VOICE_LEAVE'),
	('VOICE_CHANGE');