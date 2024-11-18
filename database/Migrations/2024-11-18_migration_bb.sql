USE next_gen_beta;

CREATE TABLE IF NOT EXISTS discord_user (
	id           BIGINT AUTO_INCREMENT              NOT NULL,
	display_name VARCHAR(255)                       NOT NULL,
	global_name  VARCHAR(255)                       NOT NULL,
	created_at   DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,

	PRIMARY KEY (id)
)
	ENGINE = InnoDB
	CHARSET = UTF8MB4;