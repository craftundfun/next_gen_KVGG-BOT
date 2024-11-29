USE kvgg_next_beta;

ALTER TABLE guild
ADD COLUMN joined_at DATETIME DEFAULT NULL;