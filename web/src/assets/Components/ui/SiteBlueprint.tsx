import * as React from "react";
import {Avatar, AvatarFallback, AvatarImage} from "@ui/avatar";
import {useDiscordUser} from "@context/DiscordUserContext";
import {useWebsiteUser} from "@context/WebsiteUserContext";
import AvatarNameCombination from "@modules/AvatarSiteBlueprint";
import {useGuild} from "@context/GuildContext";

interface BaseLayoutProps {
	children: React.ReactNode;
}

const BaseLayout: React.FC<BaseLayoutProps> = ({children}) => {
	const {discordUser} = useDiscordUser();
	const {websiteUser} = useWebsiteUser();
	const {guild} = useGuild();

	const guildLogo: string | null | undefined = guild?.icon ? guild.icon : undefined;

	return (
		<div className="flex flex-col h-screen bg-gradient-to-b from-gray-900 to-gray-800">
			<div className="relative flex items-center justify-between p-2 bg-gray-800" style={{height: '8%', minHeight: '50px', maxHeight: '50px'}}>
				<div className="flex items-center">
					<Avatar className="mt-1 w-8 h-8">
						<AvatarImage src={guildLogo}/>
						<AvatarFallback>KVGG Logo</AvatarFallback>
					</Avatar>
				</div>
				<div className="absolute left-1/2 transform -translate-x-1/2 text-white text-3xl">
					KVGG
				</div>
				<AvatarNameCombination discordUser={discordUser} websiteUser={websiteUser}/>
			</div>
			<div className="flex-grow overflow-auto">
				{children}
			</div>
		</div>
	);
};

export default BaseLayout;