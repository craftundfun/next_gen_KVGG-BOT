USE kvgg_next_beta;

DROP EVENT IF EXISTS delete_old_backend_access;
DROP TABLE IF EXISTS backend_access;

CREATE TABLE IF NOT EXISTS backend_access (
	id            BIGINT UNSIGNED AUTO_INCREMENT,
	ip_address    VARCHAR(45)  NOT NULL,
	country_code  VARCHAR(2)   NULL     DEFAULT NULL,
	country_name  VARCHAR(200) NULL     DEFAULT NULL,
	access_time   DATETIME(6)  NOT NULL DEFAULT (UTC_TIMESTAMP(6)),
	authorized    TINYINT(1)   NOT NULL,
	path          TEXT         NOT NULL,
	response_code INT          NOT NULL,
	response      TEXT         NULL     DEFAULT NULL,

	PRIMARY KEY (id)
);

# SET GLOBAL event_scheduler = ON;

CREATE EVENT delete_old_backend_access
	ON SCHEDULE EVERY 1 DAY
	DO
	DELETE
	FROM backend_access
	# only delete authorized entries
	WHERE access_time < DATE_SUB(UTC_TIMESTAMP(), INTERVAL 10 DAY) AND authorized = 1;