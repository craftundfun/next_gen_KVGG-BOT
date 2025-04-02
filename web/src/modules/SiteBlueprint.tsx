import * as React from "react";
import {Avatar, AppBar, Toolbar, Typography, Box} from "@mui/material";
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

	const guildLogo: string | null | undefined = guild?.icon ? guild.icon : undefined;

	return (
		<div className="flex flex-col h-screen bg-gradient-to-b from-gray-900 to-gray-800">
			<Box sx={{height: "100vh", overflow: "auto"}}>
				<AppBar
					position="sticky"
					sx={{
						backgroundColor: "#1f1f1f",
						zIndex: 1000,
					}}
				>
					<Toolbar sx={{display: "flex", justifyContent: "space-between", alignItems: "center"}}>
						<Avatar sx={{width: 40, height: 40}}>
							<img
								src={guildLogo}
								alt="Guild Logo"
								style={{width: "100%", height: "100%", objectFit: "contain"}}
							/>
						</Avatar>

						<Typography variant="h5" sx={{color: "white"}}>
							KVGG
						</Typography>

						<AvatarNameCombination
							discordUser={discordUser}
							websiteUser={websiteUser}
							guildDiscordUserMapping={guildDiscordUserMapping}
						/>
					</Toolbar>
				</AppBar>

				<Box sx={{flexGrow: 1, overflow: "auto", padding: 2}}>
					{children}
				</Box>
			</Box>
		</div>
	);
};

export default BaseLayout;
