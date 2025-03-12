export interface Statistic {
	discord_id: string;
	guild_id: string;
	date: string;
	online_time: string;
	stream_time: string;
	mute_time: string;
	deaf_time: string;
	message_count: string;
	command_count: string;
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