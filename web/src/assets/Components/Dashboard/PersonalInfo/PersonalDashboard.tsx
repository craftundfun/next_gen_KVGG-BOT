import {useNavigate} from "react-router-dom";
import {useDiscordUser} from "@context/DiscordUserContext";
import {useEffect, useState} from "react";
import {Statistic} from "@customTypes/Statistic";
import React from "react";
import {useGuild} from "@context/GuildContext";

function PersonalDashboard() {
	const navigate = useNavigate();

	const token = sessionStorage.getItem('jwt');
	const tokenType = sessionStorage.getItem('tokenType');

	const {discordUser} = useDiscordUser();
	const {guild} = useGuild();
	// const {websiteUser} = useWebsiteUser();

	const [statistics, setStatistics] = useState<Statistic | null>(null);
	const [loading, setLoading] = useState<boolean>(true);

	useEffect(() => {
		if (discordUser === null || guild ===null) {
			return;
		}

		const today = new Date();
		const formattedDate = today.toISOString().split('T')[0];

		// TODO remove hardcoded guild id
		fetch("/api/statistic/" + guild.guild_id + "/" + discordUser.discord_id + "/" + formattedDate.toString(), {
			method: "GET",
			headers: {
				"Content-Type": "application/json",
				Authorization: tokenType + " " + token,
			},
			credentials: "include",
		}).then(async response => {
			if (!response.ok) {
				navigate("/error");

				return null;
			}

			setStatistics(await response.json());
			setLoading(false);
		})
	}, [setStatistics, navigate, token, tokenType, discordUser, guild]);

	console.log(statistics);

	return (
		<div>
			{loading ? (
				<p>Loading...</p>
			) : (
				<div>
					<h1>Personal Dashboard</h1>
					<p>Discord ID: {discordUser?.discord_id}</p>
					<p>Global Name: {discordUser?.global_name}</p>
					<p>Created At: {discordUser?.created_at}</p>

					<h2>Statistics</h2>
					<p>Date: {statistics?.date ?? "N/A"}</p>
					<p>Online Time: {statistics?.online_time ?? 0}</p>
					<p>Stream Time: {statistics?.stream_time ?? 0}</p>
					<p>Mute Time: {statistics?.mute_time ?? 0}</p>
					<p>Deaf Time: {statistics?.deaf_time ?? 0}</p>
					<p>Message Count: {statistics?.message_count ?? 0}</p>
					<p>Command Count: {statistics?.command_count ?? 0}</p>
				</div>
			)}
		</div>
	)
}

export default PersonalDashboard;