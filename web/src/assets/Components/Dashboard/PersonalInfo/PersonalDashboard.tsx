import {useNavigate} from "react-router-dom";
import {useDiscordUser} from "@context/DiscordUserContext";
import {useEffect, useState} from "react";
import {Statistic} from "@customTypes/Statistic";
import {backendUrl} from "@modules/Constants";
import React from "react";

function PersonalDashboard() {
	const navigate = useNavigate();

	const token = sessionStorage.getItem('jwt');
	const tokenType = sessionStorage.getItem('tokenType');

	const {discordUser} = useDiscordUser();
	// const {websiteUser} = useWebsiteUser();

	const [statistics, setStatistics] = useState<Statistic | null>(null);
	const [loading, setLoading] = useState<boolean>(true);

	useEffect(() => {
		if (!discordUser?.discord_id) {
			return;
		}

		// TODO remove hardcoded guild id
		fetch(backendUrl + "/api/statistic/438689788585967616/" + discordUser.discord_id, {
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
	}, [discordUser?.discord_id, setStatistics, navigate, token, tokenType]);

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
					<p>Date: {statistics?.date.toString()}</p>
					<p>Online Time: {statistics?.online_time}</p>
					<p>Stream Time: {statistics?.stream_time}</p>
					<p>Mute Time: {statistics?.mute_time}</p>
					<p>Deaf Time: {statistics?.deaf_time}</p>
					<p>Message Count: {statistics?.message_count}</p>
					<p>Command Count: {statistics?.command_count}</p>
				</div>
			)}
		</div>
	)
}

export default PersonalDashboard;