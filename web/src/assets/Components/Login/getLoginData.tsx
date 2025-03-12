import {DiscordUser} from "@customTypes/DiscordUser";
import {WebsiteUser} from "@customTypes/WebsiteUser";
import {Guild} from "@customTypes/Guild";

function getLoginData(response: Response): [string, string, DiscordUser, WebsiteUser, Guild] | false {
	/*
	 * This function parses the response from the login request.
	 * It returns the token type, token, discord user and website user.
	 */
	const authorizationHeader = response.headers.get("Authorization");
	const discordUserHeader = response.headers.get("DiscordUser");
	const websiteUserHeader = response.headers.get("WebsiteUser");
	const guildHeader = response.headers.get("Guild");

	if (!authorizationHeader || !discordUserHeader || !websiteUserHeader || !guildHeader) {
		console.log("Error: Missing headers");

		return false;
	}

	const tokenType = authorizationHeader.split(" ")[0];
	const token = authorizationHeader.split(" ")[1];
	const discordUserFromRequest: DiscordUser = JSON.parse(discordUserHeader);
	const websiteUserFromRequest: WebsiteUser = JSON.parse(websiteUserHeader);
	const guildFromRequest: Guild = JSON.parse(guildHeader);

	return [tokenType, token, discordUserFromRequest, websiteUserFromRequest, guildFromRequest];
}

export default getLoginData;