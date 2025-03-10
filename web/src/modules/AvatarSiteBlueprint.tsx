import {DiscordUser} from "@customTypes/DiscordUser";
import {WebsiteUser} from "@customTypes/WebsiteUser";
import React from "react";
import {Spinner} from "@ui/spinner";
import {Avatar, AvatarImage} from "@ui/avatar";

type Props = {
	discordUser: DiscordUser | null;
	websiteUser: WebsiteUser | null;
};

function AvatarNameCombination({discordUser, websiteUser}: Props) {
	return (
		discordUser && websiteUser ? (
			<div className="flex items-center">
				<div className="text-white">
					<div>{discordUser?.global_name || "NA"}</div>
					<div className="text-sm">{websiteUser?.email || "NA"}</div>
				</div>
				<Avatar className="ml-2 mt-1 w-8 h-8">
					<AvatarImage src={''}/>
				</Avatar>
			</div>
		) : (
			<Spinner size="large"/>
		)
	);
}

export default AvatarNameCombination;