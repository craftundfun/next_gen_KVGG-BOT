USE kvgg_next_beta;

DROP TABLE IF EXISTS category_guild_mapping;
# DROP TABLE IF EXISTS category_channel_mapping;
DROP TABLE IF EXISTS category;

CREATE TABLE IF NOT EXISTS category (
	category_id BIGINT UNSIGNED UNIQUE NOT NULL,
	name        VARCHAR(255)           NOT NULL,
	deleted_at  DATETIME               NULL DEFAULT NULL,

	PRIMARY KEY (category_id)
)

	ENGINE = InnoDB
	CHARSET = UTF8MB4;

# CREATE TABLE IF NOT EXISTS category_channel_mapping (
# 	category_id BIGINT UNSIGNED NOT NULL,
# 	channel_id  BIGINT UNSIGNED NOT NULL,
#
# 	PRIMARY KEY (category_id, channel_id),
# 	FOREIGN KEY (category_id) REFERENCES category(category_id),
# 	FOREIGN KEY (channel_id) REFERENCES channel(channel_id)
# )
#
# 	ENGINE = InnoDB
# 	CHARSET = UTF8MB4;

CREATE TABLE IF NOT EXISTS category_guild_mapping (
	category_id BIGINT UNSIGNED NOT NULL,
	guild_id    BIGINT UNSIGNED NOT NULL,

	PRIMARY KEY (category_id, guild_id),
	FOREIGN KEY (category_id) REFERENCES category(category_id),
	FOREIGN KEY (guild_id) REFERENCES guild(guild_id)
)

	ENGINE = InnoDB
	CHARSET = UTF8MB4;

DROP PROCEDURE IF EXISTS FindMissingCategories;

DELIMITER $$

CREATE PROCEDURE FindMissingCategories(IN categoryIds TEXT, OUT missing_categories TEXT)
BEGIN
	DROP TEMPORARY TABLE IF EXISTS temp_category_id_list;

	-- Create a temporary table to hold the provided channel IDs
	CREATE TEMPORARY TABLE temp_category_id_list (
		category_id BIGINT UNSIGNED NOT NULL
	);

	-- Insert the channel IDs into the temporary table, ensuring no duplicates
	SET @sql = CONCAT(
			'INSERT INTO temp_category_id_list (category_id) VALUES ',
			categoryIds
			   );
	PREPARE stmt FROM @sql;
	EXECUTE stmt;
	DEALLOCATE PREPARE stmt;

	-- Retrieve the missing channels (those not in the 'channel' table)
	-- Using GROUP_CONCAT to combine all missing channel IDs into a single string
	SET @missingCategories = (SELECT CONCAT('(', GROUP_CONCAT(t.category_id), ')') AS category_ids
							  FROM temp_category_id_list t
									   LEFT JOIN category c ON t.category_id = c.category_id
							  WHERE c.category_id IS NULL);

	-- Set the result into the output variable (missing_channels)
	SET missing_categories = @missingCategories;

	-- Clean up by dropping the temporary table
	DROP TEMPORARY TABLE temp_category_id_list;

END $$

DELIMITER ;

DROP TEMPORARY TABLE IF EXISTS temp_channel_id_list;

CALL FindMissingCategories('(1), (2), (3), (4), (5)', @missing_categories);
SELECT @missing_categories;