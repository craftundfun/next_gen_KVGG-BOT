USE kvgg_next_beta;

DROP TABLE IF EXISTS website_user;

CREATE TABLE IF NOT EXISTS website_user (
	# same primary key as discord_user
	discord_id BIGINT UNSIGNED PRIMARY KEY,
	created_at TIMESTAMP    DEFAULT CURRENT_TIMESTAMP NOT NULL,
	deleted_at TIMESTAMP                              NULL,
	email      VARCHAR(255) DEFAULT NULL              NULL,

	# if the user gets lost, we don't need the user for the website
	FOREIGN KEY (discord_id) REFERENCES discord_user(discord_id) ON DELETE CASCADE
)
	ENGINE = InnoDB
	DEFAULT CHARSET = utf8mb4;