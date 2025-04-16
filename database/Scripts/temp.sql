USE kvgg_next_beta;

SELECT h.id, h.time, e.type, e.id
FROM history h
		 INNER JOIN discord_user d ON h.discord_id = d.discord_id
		 INNER JOIN event e ON e.id = h.event_id
WHERE d.discord_id = 416967436617777163 AND h.guild_id = 438689788585967616
ORDER BY h.id DESC;

DELETE
FROM history
WHERE id IN
	  (9611, 9466, 9465, 9350, 9349, 9210, 9209, 9188, 9187, 9184, 9183, 9180, 9179, 9176, 9175, 9152, 9151, 9142, 9141,
	   9130, 9129)