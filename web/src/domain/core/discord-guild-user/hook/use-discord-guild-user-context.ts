import {discordGuildUserContext} from "@/domain/core/discord-guild-user/context/discord-guild-user-context.ts";
import type {DiscordGuildUserContext} from "@/domain/core/discord-guild-user/context/discord-guild-user-context.ts";
import {useContext} from "react";

function useDiscordGuildUserContext(): DiscordGuildUserContext {
	const context = useContext<DiscordGuildUserContext | undefined>(discordGuildUserContext);

	if (!context) {
		throw new Error("useDiscordGuildUser must be used within a DiscordGuildUserProvider");
	}

	return context;
}

export default useDiscordGuildUserContext;