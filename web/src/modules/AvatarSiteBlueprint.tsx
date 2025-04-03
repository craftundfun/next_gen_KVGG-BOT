import {DiscordUser} from "@customTypes/DiscordUser";
import {WebsiteUser} from "@customTypes/WebsiteUser";
import {GuildDiscordUserMapping} from "@customTypes/GuildDiscordUserMapping";
import React from "react";
import {Avatar, CircularProgress} from "@mui/material";

type Props = {
	discordUser: DiscordUser | null;
	websiteUser: WebsiteUser | null;
	guildDiscordUserMapping: GuildDiscordUserMapping | null;
};

function AvatarNameCombination({discordUser, websiteUser, guildDiscordUserMapping}: Props) {
	return (
		discordUser && websiteUser ? (
			<div className="flex items-center">
				<div className="text-white">
					<div>{discordUser?.global_name || "NA"}</div>
					<div className="text-sm">{websiteUser?.email || "NA"}</div>
				</div>

				<Avatar
					className="ml-2 mt-1 w-8 h-8"
					src={guildDiscordUserMapping?.profile_picture || ""}
					alt="User Avatar"
				/>
			</div>
		) : (
			<CircularProgress size={24}/>
		)
	);
}

export default AvatarNameCombination;
