USE kvgg_next_beta;

DROP TABLE IF EXISTS website_user;

CREATE TABLE IF NOT EXISTS website_user (
	# same primary key as discord_user
	discord_id    BIGINT UNSIGNED PRIMARY KEY,
	created_at    DATETIME(6)  NOT NULL DEFAULT (UTC_TIMESTAMP(6)),
	deleted_at    DATETIME(6)  NULL     DEFAULT (UTC_TIMESTAMP(6)),
	email         VARCHAR(255) NULL     DEFAULT NULL,
	refresh_token TEXT         NULL     DEFAULT NULL,

	# if the user gets lost, we don't need the user for the website
	FOREIGN KEY (discord_id) REFERENCES discord_user(discord_id)
)
	ENGINE = InnoDB
	DEFAULT CHARSET = utf8mb4;