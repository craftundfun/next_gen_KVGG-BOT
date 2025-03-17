import React, {useEffect, useState} from "react";
import {Statistic} from "@customTypes/Statistic";
import {useNavigate} from "react-router-dom";
import {useDiscordUser} from "@context/DiscordUserContext";
import {useGuild} from "@context/GuildContext";
import {LineChart} from "@mui/x-charts";

function StatisticGraph() {
	const navigate = useNavigate();
	const token = sessionStorage.getItem('jwt');
	const tokenType = sessionStorage.getItem('tokenType');
	const {discordUser} = useDiscordUser();
	const {guild} = useGuild();

	const [statistics, setStatistics] = useState<Statistic[] | null>(null);
	const [endDate, setEndDate] = useState<Date>(new Date());
	const [startDate, setStartDate] = useState<Date>(() => {
		const initialEndDate = new Date();
		initialEndDate.setDate(initialEndDate.getDate() - 5);
		return initialEndDate;
	});

	useEffect(() => {
			if (!discordUser || !guild) return;

			fetch(`/api/statistic/${guild.guild_id}/${discordUser.discord_id}/${startDate.toISOString().split('T')[0]}/${endDate.toISOString().split('T')[0]}`, {
				method: "GET",
				headers: {
					"Content-Type": "application/json",
					Authorization: `${tokenType} ${token}`,
				},
				credentials: "include",
			}).then(async (response) => {
				if (!response.ok) {
					navigate("/error");

					return;
				}

				if (response.status === 204) {
					setStatistics(null);

					return;
				}

				const data = await response.json();
				setStatistics(data);
			})
		},
		[discordUser, guild, navigate, token, tokenType, startDate, endDate]
	);

	return (
		<div>
			{statistics && statistics.length > 0 ? (
				<LineChart
					xAxis={[{
						scaleType: "time",
						data: statistics
							.sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime()) // Sortiere nach Datum
							.map(stat => new Date(stat.date)) // Verwende das vollständige Datum für die x-Achse
					}]}
					series={[{ data: statistics.map(stat => Number(stat.online_time)), label: "OnlineTime" }]}
					width={600}
					height={400}
				/>

			) : (
				<p>Keine Daten verfügbar</p>
			)}
		</div>
	);
}

export default StatisticGraph;