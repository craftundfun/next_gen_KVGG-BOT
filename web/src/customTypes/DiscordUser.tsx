// import {WebsiteUser} from "./WebsiteUser";

export interface DiscordUser {
	discord_id: number;
	global_name: string;
	created_at: string;
	profile_picture: string;
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
			profile_picture: data.profile_picture,
		};
	} catch (error) {
		console.error(error);

		return null;
	}
}

export default parseDiscordUser;