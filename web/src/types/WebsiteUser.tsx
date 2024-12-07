//import {DiscordUser} from "./DiscordUser";

export interface WebsiteUser {
	discord_id: number;
	created_at: string;
	deleted_at: string;
	email: string;
	//discordUser?: DiscordUser;
}

function parseWebsiteUser(data: any): WebsiteUser | null {
	/*
	 * This function parses the DiscordUser object.
	 */
	try {
		return {
			discord_id: data.discord_id,
			created_at: data.created_at,
			deleted_at: data.deleted_at,
			email: data.email,
		};
	} catch (error) {
		console.error(error);

		return null;
	}
}

export default parseWebsiteUser;