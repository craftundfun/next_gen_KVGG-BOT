SET FOREIGN_KEY_CHECKS = 0;

SELECT CONCAT('DROP TABLE IF EXISTS ', GROUP_CONCAT(table_name), ';')
INTO @sql
FROM information_schema.tables
WHERE table_schema = 'kvgg_next_beta';

PREPARE stmt FROM @sql;

EXECUTE stmt;

DEALLOCATE PREPARE stmt;

SET FOREIGN_KEY_CHECKS = 1;
