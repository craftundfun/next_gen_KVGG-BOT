interface GuildDiscordUserMapping {
	guild_id: string,
	discord_id: string,
	display_name: string,
	profile_picture: string | null,
	joined_at: string,
	left_at: string | null,
}