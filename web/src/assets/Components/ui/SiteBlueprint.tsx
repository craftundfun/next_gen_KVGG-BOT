import * as React from "react";
import {Avatar, AvatarFallback, AvatarImage} from "@ui/avatar";
import {useDiscordUser} from "@context/DiscordUserContext";
import {useWebsiteUser} from "@context/WebsiteUserContext";
import AvatarNameCombination from "@modules/AvatarSiteBlueprint";
import {useGuild} from "@context/GuildContext";
import {useGuildDiscordUserMapping} from "@context/GuildDiscordUserMappingContext";

interface BaseLayoutProps {
	children: React.ReactNode;
}

const BaseLayout: React.FC<BaseLayoutProps> = ({children}) => {
	const {discordUser} = useDiscordUser();
	const {websiteUser} = useWebsiteUser();
	const {guild} = useGuild();
	const {guildDiscordUserMapping} = useGuildDiscordUserMapping();

	console.group();
	console.log("DiscordUser", discordUser);
	console.log("WebsiteUser", websiteUser);
	console.log("Guild", guild);
	console.log("GuildDiscordUserMapping", guildDiscordUserMapping);
	console.groupEnd();

	const guildLogo: string | null | undefined = guild?.icon ? guild.icon : undefined;

	return (
		<div className="flex flex-col h-screen bg-gradient-to-b from-gray-900 to-gray-800">
			<div
				className="relative flex items-center justify-between p-2 bg-gray-800 w-full"
				style={{height: "8%", minHeight: "50px", maxHeight: "50px"}}
			>
				<div className="flex items-center w-1/3">
					<Avatar className="w-8 h-8">
						<AvatarImage src={guildLogo}/>
						<AvatarFallback>KVGG Logo</AvatarFallback>
					</Avatar>
				</div>
				<div className="flex-1 text-center text-white text-3xl">KVGG</div>
				<div className="flex items-center justify-end w-1/3">
					<AvatarNameCombination
						discordUser={discordUser}
						websiteUser={websiteUser}
						guildDiscordUserMapping={guildDiscordUserMapping}
					/>
				</div>
			</div>
			<div className="flex-grow overflow-auto">{children}</div>
		</div>
	);
};

export default BaseLayout;