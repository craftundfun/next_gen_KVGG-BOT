USE kvgg_next_beta;

DROP TABLE IF EXISTS ip_address;

CREATE TABLE IF NOT EXISTS ip_address (
	id           BIGINT UNSIGNED AUTO_INCREMENT,
	ip_address   VARCHAR(45)  NOT NULL,
	country_code VARCHAR(2)   NULL     DEFAULT NULL,
	country_name VARCHAR(200) NULL     DEFAULT NULL,
	access_time  DATETIME(6)  NOT NULL DEFAULT (UTC_TIMESTAMP(6)),
	authorized   TINYINT(1)   NOT NULL,
	path         TEXT         NOT NULL,

	PRIMARY KEY (id)
);

CREATE INDEX idx_ip_address ON ip_address(ip_address);