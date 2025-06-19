import type DiscordGuildUser from "@/domain/core/discord-guild-user/@types/discord-guild-user.ts";
import {createContext} from "react";

export interface DiscordGuildUserContext {
	discordGuildUser: DiscordGuildUser | null;
}

export const discordGuildUserContext = createContext<DiscordGuildUserContext | undefined>(undefined);
