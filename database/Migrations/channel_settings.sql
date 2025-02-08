USE kvgg_next_beta;

CREATE TABLE IF NOT EXISTS channel_setting (
	id         BIGINT UNSIGNED AUTO_INCREMENT NOT NULL,
	channel_id BIGINT UNSIGNED                NOT NULL,
	track_time TINYINT(1)                     NOT NULL DEFAULT 0,

	PRIMARY KEY (id),
	FOREIGN KEY (channel_id) REFERENCES channel(channel_id)
)
	ENGINE = InnoDB
	CHARSET = UTF8MB4;