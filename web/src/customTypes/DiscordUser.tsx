// import {WebsiteUser} from "./WebsiteUser";

export interface DiscordUser {
	discord_id: string;
	global_name: string;
	created_at: string;
	//websiteUser?: WebsiteUser;
}

function parseDiscordUser(data: any): DiscordUser | null {
	/*
	 * This function parses the DiscordUser object.
	 */
	try {
		console.log("Data: ", data, data.created_at, data.discord_id, data.global_name, data.profile_picture);

		return {
			discord_id: data.discord_id,
			global_name: data.global_name,
			created_at: data.created_at,
		};
	} catch (error) {
		console.error(error);

		return null;
	}
}

export default parseDiscordUser;