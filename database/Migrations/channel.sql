USE kvgg_next_beta;

DROP TABLE IF EXISTS channel;

CREATE TABLE IF NOT EXISTS channel (
	channel_id BIGINT UNSIGNED UNIQUE                   NOT NULL,
	name       VARCHAR(255)                             NOT NULL,
	type       ENUM ('text', 'voice', 'stage', 'forum') NOT NULL,
	# see categories
	# deleted_at DATETIME DEFAULT NULL                    NULL,
	guild_id   BIGINT UNSIGNED                          NOT NULL,

	PRIMARY KEY (channel_id),
	FOREIGN KEY (guild_id) REFERENCES guild(guild_id) ON DELETE CASCADE
)
	ENGINE = InnoDB
	CHARSET = UTF8MB4;