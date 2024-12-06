import {DiscordUser} from "./DiscordUser";

export interface WebsiteUser {
	discord_id: number;
	global_name: string;
	created_at: string;
	profile_picture: string;
	discordUser?: DiscordUser;
}