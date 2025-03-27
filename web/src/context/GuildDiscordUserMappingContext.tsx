import React, {createContext, useContext, useState, ReactNode, useEffect} from 'react';
import {useGuild} from "@context/GuildContext";
import {useDiscordUser} from "@context/DiscordUserContext";
import {GuildDiscordUserMapping} from "@customTypes/GuildDiscordUserMapping";

interface GuildDiscordUserMappingContextType {
	guildDiscordUserMapping: GuildDiscordUserMapping | null;
	setGuildDiscordUserMapping: (mapping: GuildDiscordUserMapping) => void;
}

const GuildDiscordUserMappingContext = createContext<GuildDiscordUserMappingContextType | undefined>(undefined);

interface Props {
	children: ReactNode;
}

export const GuildDiscordUserMappingProvider: React.FC<Props> = ({children}) => {
	const {discordUser} = useDiscordUser();
	const {guild} = useGuild();

	const [guildDiscordUserMapping, setGuildDiscordUserMappingState] = useState<GuildDiscordUserMapping | null>(() => {
		const storedMapping = sessionStorage.getItem('guildDiscordUserMapping');

		if (storedMapping === null) {
			return null;
		}

		const mapping: GuildDiscordUserMapping = JSON.parse(storedMapping);

		if (mapping.guild_id === null || mapping.guild_id === undefined) {
			return null;
		}

		return mapping;
	});

	const setGuildDiscordUserMapping = (mapping: GuildDiscordUserMapping) => {
		sessionStorage.setItem('guildDiscordUserMapping', JSON.stringify(mapping));

		setGuildDiscordUserMappingState(mapping);
	};

	useEffect(() => {
		if (!discordUser || !guild) return;

		fetch(`/api/guildDiscordUserMapping/${guild.guild_id}/${discordUser.discord_id}`, {
			method: "GET",
			headers: {
				"Content-Type": "application/json",
			},
			credentials: "include",
		})
			.then((response) => response.json())
			.then((data) => {
				if (data) {
					setGuildDiscordUserMapping(data);
				}
			})
			.catch((error) => {
				console.error("Error fetching Discord user:", error);
			});
	}, [discordUser, guild]);


	return (
		<GuildDiscordUserMappingContext.Provider value={{guildDiscordUserMapping, setGuildDiscordUserMapping}}>
			{children}
		</GuildDiscordUserMappingContext.Provider>
	);
};

export const useGuildDiscordUserMapping = (): GuildDiscordUserMappingContextType => {
	const context = useContext(GuildDiscordUserMappingContext);

	if (!context) {
		throw new Error('useDiscordUser must be used within a DiscordUserProvider');
	}

	return context;
};