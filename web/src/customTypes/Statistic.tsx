export interface Statistic {
	discord_id: number;
	guild_id: number;
	date: Date;
	online_time: number;
	stream_time: number;
	mute_time: number;
	deaf_time: number;
	message_count: number;
	command_count: number;
}

function parseStatistic(data: any): Statistic | null {
	/*
	 * This function parses the Statistic object.
	 */
	try {
		return {
			discord_id: data.discord_id,
			guild_id: data.guild_id,
			date: data.date,
			online_time: data.online_time,
			stream_time: data.stream_time,
			mute_time: data.mute_time,
			deaf_time: data.deaf_time,
			message_count: data.message_count,
			command_count: data.command_count,
		};
	} catch (error) {
		console.error(error);

		return null;
	}
}

export default parseStatistic;