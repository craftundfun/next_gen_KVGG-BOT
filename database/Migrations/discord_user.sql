USE kvgg_next_beta;

DROP TABLE IF EXISTS discord_user;

CREATE TABLE IF NOT EXISTS discord_user (
	discord_id  BIGINT UNSIGNED UNIQUE NOT NULL,
	global_name VARCHAR(255)           NOT NULL,
	created_at  DATETIME(6)            NOT NULL DEFAULT (UTC_TIMESTAMP(6)),
	# guild specific pictures are possible
	# profile_picture TEXT                   NULL     DEFAULT NULL,

	PRIMARY KEY (discord_id)
)
	ENGINE = InnoDB
	CHARSET = UTF8MB4;