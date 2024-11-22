USE next_gen_beta;

DROP PROCEDURE IF EXISTS FindMissingChannels;

DELIMITER $$

CREATE PROCEDURE FindMissingChannels(IN channelIds TEXT, OUT missing_channels TEXT)
BEGIN
	DROP TEMPORARY TABLE IF EXISTS temp_channel_id_list;

	-- Create a temporary table to hold the provided channel IDs
	CREATE TEMPORARY TABLE temp_channel_id_list (
		channel_id BIGINT UNSIGNED NOT NULL
	);

	-- Insert the channel IDs into the temporary table, ensuring no duplicates
	SET @sql = CONCAT(
			'INSERT INTO temp_channel_id_list (channel_id) VALUES ',
			channelIds
			   );
	PREPARE stmt FROM @sql;
	EXECUTE stmt;
	DEALLOCATE PREPARE stmt;

	-- Retrieve the missing channels (those not in the 'channel' table)
	-- Using GROUP_CONCAT to combine all missing channel IDs into a single string
	SET @missingChannels = (SELECT CONCAT('(', GROUP_CONCAT(t.channel_id), ')') AS channel_ids
							FROM temp_channel_id_list t
									 LEFT JOIN channel c ON t.channel_id = c.channel_id
							WHERE c.channel_id IS NULL);

	-- Set the result into the output variable (missing_channels)
	SET missing_channels = @missingChannels;

	-- Clean up by dropping the temporary table
	DROP TEMPORARY TABLE temp_channel_id_list;

END $$

DELIMITER ;

DROP TEMPORARY TABLE IF EXISTS temp_channel_id_list;
