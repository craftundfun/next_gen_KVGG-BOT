USE kvgg_next_beta;

CREATE TABLE game (
	game_id BIGINT UNSIGNED NOT NULL,
	name    TEXT            NOT NULL,

	PRIMARY KEY (game_id)
)
	ENGINE = InnoDB
	CHARSET = UTF8MB4;

CREATE TABLE game_mapping (
	primary_game_id   BIGINT UNSIGNED        NOT NULL,
	# every game will be in the secondary_game_id column
	# also every game can only be the secondary_game_id of one primary_game_id
	# game 1, 2, 3 with 1 = 2, 3
	# primary_game_id = 1, secondary_game_id = 1
	# primary_game_id = 1, secondary_game_id = 2
	# primary_game_id = 3, secondary_game_id = 3
	secondary_game_id BIGINT UNSIGNED UNIQUE NOT NULL,

	PRIMARY KEY (primary_game_id, secondary_game_id),
	FOREIGN KEY (primary_game_id) REFERENCES game(game_id) ON DELETE CASCADE,
	FOREIGN KEY (secondary_game_id) REFERENCES game(game_id) ON DELETE CASCADE
)
	ENGINE = InnoDB
	CHARSET = UTF8MB4;

CREATE TABLE activity_history (
	id         BIGINT UNSIGNED AUTO_INCREMENT NOT NULL,
	discord_id BIGINT UNSIGNED                NOT NULL,
	game_id    BIGINT UNSIGNED                NOT NULL,
	event_id   BIGINT UNSIGNED                NOT NULL,

	PRIMARY KEY (id),
	FOREIGN KEY (discord_id) REFERENCES discord_user(discord_id) ON DELETE CASCADE,
	FOREIGN KEY (game_id) REFERENCES game_mapping(secondary_game_id) ON DELETE CASCADE,
	FOREIGN KEY (event_id) REFERENCES event(id) ON DELETE CASCADE,

	# only the activity start and end events are allowed
	CHECK ( event_id = 10 OR event_id = 11 )
)
	ENGINE = InnoDB
	CHARSET = UTF8MB4;