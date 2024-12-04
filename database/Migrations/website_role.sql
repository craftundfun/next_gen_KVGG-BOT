USE kvgg_next_beta;

DROP TABLE IF EXISTS website_role;

CREATE TABLE IF NOT EXISTS website_role (
	role_id    INT UNSIGNED AUTO_INCREMENT UNIQUE NOT NULL,
	role_name  VARCHAR(255) UNIQUE                NOT NULL,
	created_at TIMESTAMP                                   DEFAULT CURRENT_TIMESTAMP NOT NULL,
	deleted_at TIMESTAMP                          NULL,
	priority   INT UNSIGNED                       NOT NULL DEFAULT 0,

	PRIMARY KEY (role_id)
)

	ENGINE = InnoDB
	DEFAULT CHARSET = utf8mb4;

DROP TABLE IF EXISTS website_role_user_mapping;

CREATE TABLE IF NOT EXISTS website_role_user_mapping (
	role_id    INT UNSIGNED                        NOT NULL,
	discord_id BIGINT UNSIGNED                     NOT NULL,

	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
	deleted_at TIMESTAMP                           NULL,

	PRIMARY KEY (role_id, discord_id),
	FOREIGN KEY (role_id) REFERENCES website_role(role_id),
	FOREIGN KEY (discord_id) REFERENCES website_user(discord_id)
)

	ENGINE = InnoDB
	DEFAULT CHARSET = utf8mb4;
