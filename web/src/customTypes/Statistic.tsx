export interface Statistic {
	discord_id: string;
	guild_id: string;
	date: string;
	online_time: number;
	stream_time: number;
	mute_time: number;
	deaf_time: number;
	message_count: number;
	command_count: number;
}