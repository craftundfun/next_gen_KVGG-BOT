USE kvgg_next_beta;

DROP TABLE IF EXISTS discord_user;

CREATE TABLE IF NOT EXISTS discord_user (
	discord_id      BIGINT UNSIGNED UNIQUE NOT NULL,
	global_name     VARCHAR(255)           NOT NULL,
	created_at      DATETIME DEFAULT NOW() NOT NULL,
	profile_picture TEXT                   NOT NULL,

	PRIMARY KEY (discord_id)
)
	ENGINE = InnoDB
	CHARSET = UTF8MB4;