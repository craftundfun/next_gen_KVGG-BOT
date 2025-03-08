USE kvgg_next_beta;

DROP TABLE IF EXISTS website_role_user_mapping;
DROP TABLE IF EXISTS website_role;

CREATE TABLE IF NOT EXISTS website_role (
	role_id    INT UNSIGNED AUTO_INCREMENT UNIQUE NOT NULL,
	role_name  VARCHAR(255) UNIQUE                NOT NULL,
	created_at DATETIME(6)                        NOT NULL DEFAULT (UTC_TIMESTAMP(6)),
	priority   INT UNSIGNED                       NOT NULL DEFAULT 0,

	CHECK ( priority >= 0 ),
	CHECK ( priority <= 100),

	PRIMARY KEY (role_id)
)

	ENGINE = InnoDB
	DEFAULT CHARSET = utf8mb4;

INSERT INTO website_role (role_name, priority)
VALUES ('Administrator', 100),
	('Moderator', 50),
	('User', 0);

CREATE TABLE IF NOT EXISTS website_role_user_mapping (
	role_id    INT UNSIGNED    NOT NULL,
	discord_id BIGINT UNSIGNED NOT NULL,
	created_at DATETIME(6)     NOT NULL DEFAULT (UTC_TIMESTAMP(6)),

	PRIMARY KEY (role_id, discord_id),
	FOREIGN KEY (role_id) REFERENCES website_role(role_id),
	FOREIGN KEY (discord_id) REFERENCES website_user(discord_id)
)

	ENGINE = InnoDB
	DEFAULT CHARSET = utf8mb4;
