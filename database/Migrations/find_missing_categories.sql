USE kvgg_next_beta;

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