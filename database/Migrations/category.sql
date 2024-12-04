USE kvgg_next_beta;

DROP TABLE IF EXISTS category;

CREATE TABLE IF NOT EXISTS category (
	category_id BIGINT UNSIGNED UNIQUE NOT NULL,
	name        VARCHAR(255)           NOT NULL,
	deleted_at  DATETIME               NULL DEFAULT NULL,
	guild_id    BIGINT UNSIGNED        NOT NULL,

	PRIMARY KEY (category_id),
	FOREIGN KEY (guild_id) REFERENCES guild(guild_id)
)

	ENGINE = InnoDB
	CHARSET = UTF8MB4;