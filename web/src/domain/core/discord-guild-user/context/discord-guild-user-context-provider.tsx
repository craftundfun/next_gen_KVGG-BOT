import {discordGuildUserContext} from "@/domain/core/discord-guild-user/context/discord-guild-user-context.ts";
import fetchDiscordGuildUser from "@/domain/core/discord-guild-user/http/fetch-discord-guild-user.ts";
import useWebsiteUserContext from "@/domain/core/website-user/hook/use-website-user-context.ts";
import {useQuery} from "@tanstack/react-query";
import * as React from "react";

function DiscordGuildUserContextProvider({children}: React.PropsWithChildren): React.ReactNode {
	const {websiteUser} = useWebsiteUserContext();
	const discordUserId = websiteUser?.discord_id ?? null;

	const {data} = useQuery({
		queryKey: ['discordGuildUser', discordUserId],
		queryFn: () => fetchDiscordGuildUser(discordUserId),
	});

	// TODO: Make method to change discordGuildUserId to fetch different guild data for the same user

	return <discordGuildUserContext.Provider value={{discordGuildUser: data ?? null}}>
		{children}
	</discordGuildUserContext.Provider>
}

export default DiscordGuildUserContextProvider;