USE kvgg_next_beta;

DROP TABLE IF EXISTS website_user;

CREATE TABLE IF NOT EXISTS website_user (
	# same primary key as discord_user
	discord_id BIGINT UNSIGNED PRIMARY KEY,
	created_at TIMESTAMP    DEFAULT CURRENT_TIMESTAMP NOT NULL,
	deleted_at TIMESTAMP                              NULL,
	email      VARCHAR(255) DEFAULT NULL              NULL,

	FOREIGN KEY (discord_id) REFERENCES discord_user(discord_id)
)
	ENGINE = InnoDB
	DEFAULT CHARSET = utf8mb4;