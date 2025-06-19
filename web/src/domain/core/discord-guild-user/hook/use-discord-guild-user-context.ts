import {discordGuildUserContext} from "@/domain/core/discord-guild-user/context/discord-guild-user-context.ts";
import type {DiscordGuildUserContext} from "@/domain/core/discord-guild-user/context/discord-guild-user-context.ts";
import {useContext} from "react";

function useDiscordGuildUserContext(): DiscordGuildUserContext {
	const context = useContext<DiscordGuildUserContext | undefined>(discordGuildUserContext);

	if (!context) {
		throw new Error("useWebsiteUser must be used within a WebsiteUserProvider");
	}

	return context;
}

export default useDiscordGuildUserContext;