import type DiscordGuildUser from "@/domain/core/discord-guild-user/@types/discord-guild-user.ts";

async function fetchDiscordGuildUser(discordUserId: string|null): Promise<DiscordGuildUser|null> {
	if (!discordUserId) {
		return null;
	}

	const response = await fetch(`/api/discordUser/${discordUserId}`, {
		method: 'GET',
		credentials: 'include',
		headers: {
			'Content-Type': 'application/json',
		}
	});

	if (!response.ok) {
		throw new Error('Network response was not ok');
	}

	const data: unknown = await response.json();

	if (!data) {
		throw new Error('No user data found');
	}

	return data as DiscordGuildUser;
}

export default fetchDiscordGuildUser;