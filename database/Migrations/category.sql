USE kvgg_next_beta;

DROP TABLE IF EXISTS category;

CREATE TABLE IF NOT EXISTS category (
	category_id BIGINT UNSIGNED UNIQUE NOT NULL,
	name        VARCHAR(255)           NOT NULL,
	# we can delete the category.
	# if it's gone on discord, it will never come back
	# deleted_at  DATETIME               NULL DEFAULT NULL,
	guild_id    BIGINT UNSIGNED        NOT NULL,

	PRIMARY KEY (category_id),
	# if the guild gets deleted, we delete the corresponding categories
	FOREIGN KEY (guild_id) REFERENCES guild(guild_id) ON DELETE CASCADE
)

	ENGINE = InnoDB
	CHARSET = UTF8MB4;