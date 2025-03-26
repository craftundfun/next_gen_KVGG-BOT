USE kvgg_next_beta;

DROP TRIGGER IF EXISTS activity_insert;
DROP TRIGGER IF EXISTS activity_history_insert;
DROP TRIGGER IF EXISTS activity_history_update;

DROP TABLE IF EXISTS activity_history;
DROP TABLE IF EXISTS activity_mapping;
DROP TABLE IF EXISTS activity_statistic;
DROP TABLE IF EXISTS activity;

CREATE TABLE activity (
	# not all activities have an id given by Discord
	id                   BIGINT UNSIGNED AUTO_INCREMENT NOT NULL,
	external_activity_id BIGINT UNSIGNED UNIQUE         NULL DEFAULT NULL,
	name                 VARCHAR(255)                   NOT NULL,

	PRIMARY KEY (id)
)
	ENGINE = InnoDB
	CHARSET = UTF8MB4;

CREATE TABLE activity_mapping (
	primary_activity_id   BIGINT UNSIGNED        NOT NULL,
	# every activity will be in the secondary_activity_id column
	# also every game can only be the secondary_activity_id of one primary_activity_id
	# game 1, 2, 3 with 1 = 2, 3
	# primary_activity_id = 1, secondary_activity_id = 1
	# primary_activity_id = 1, secondary_activity_id = 2
	# primary_activity_id = 3, secondary_activity_id = 3
	secondary_activity_id BIGINT UNSIGNED UNIQUE NOT NULL,

	PRIMARY KEY (primary_activity_id, secondary_activity_id),
	FOREIGN KEY (primary_activity_id) REFERENCES activity(id),
	FOREIGN KEY (secondary_activity_id) REFERENCES activity(id)
)
	ENGINE = InnoDB
	CHARSET = UTF8MB4;

CREATE TABLE activity_history (
	id                  BIGINT UNSIGNED AUTO_INCREMENT NOT NULL,
	discord_id          BIGINT UNSIGNED                NOT NULL,
	guild_id            BIGINT UNSIGNED                NOT NULL,
	primary_activity_id BIGINT UNSIGNED                NOT NULL,
	event_id            BIGINT UNSIGNED                NOT NULL,
	time                DATETIME(6)                    NOT NULL DEFAULT (UTC_TIMESTAMP(6)),

	PRIMARY KEY (id),
	FOREIGN KEY (discord_id) REFERENCES discord_user(discord_id),
	FOREIGN KEY (guild_id) REFERENCES guild(guild_id),
	FOREIGN KEY (primary_activity_id) REFERENCES activity(id),
	FOREIGN KEY (event_id) REFERENCES event(id),

	# only the activity start and end events are allowed
	CHECK ( event_id = 10 OR event_id = 11 )
)
	ENGINE = InnoDB
	CHARSET = UTF8MB4;

# automatically create the mapping for the activity with itself
CREATE TRIGGER activity_insert
	AFTER INSERT
	ON activity
	FOR EACH ROW
BEGIN
	INSERT INTO activity_mapping (primary_activity_id, secondary_activity_id) VALUES (NEW.id, NEW.id);
END;

# when the given key is not a primary id from the mapping table, the insert has to fail
# we only want the primary games listed in the history
CREATE TRIGGER activity_history_insert
	BEFORE INSERT
	ON activity_history
	FOR EACH ROW
BEGIN
	IF NOT EXISTS(SELECT 1
				  FROM activity_mapping
				  WHERE primary_activity_id = NEW.primary_activity_id)
	THEN
		SIGNAL SQLSTATE '45000'
			SET MESSAGE_TEXT =
					'The given primary activity id is not a primary activity! Find the primary activities in the activity_mapping table first.';
	END IF;
end;

# same for history update
CREATE TRIGGER activity_history_update
	BEFORE UPDATE
	ON activity_history
	FOR EACH ROW
BEGIN
	IF NOT EXISTS(SELECT 1
				  FROM activity_mapping
				  WHERE primary_activity_id = NEW.primary_activity_id)
	THEN
		SIGNAL SQLSTATE '45000'
			SET MESSAGE_TEXT =
					'The given primary activity id is not a primary activity! Find the primary activities in the activity_mapping table first.';
	END IF;
end;