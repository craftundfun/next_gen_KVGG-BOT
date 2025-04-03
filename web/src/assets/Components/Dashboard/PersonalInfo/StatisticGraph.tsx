import React, {useEffect, useState} from "react";
import {Statistic} from "@customTypes/Statistic";
import {useNavigate} from "react-router-dom";
import {useDiscordUser} from "@context/DiscordUserContext";
import {useGuild} from "@context/GuildContext";
import {AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend} from "recharts";

function StatisticGraph() {
	const navigate = useNavigate();
	const {discordUser} = useDiscordUser();
	const {guild} = useGuild();

	const [statistics, setStatistics] = useState<Statistic[] | null>(null);
	const [endDate] = useState<Date>(new Date());
	const [startDate] = useState<Date>(() => {
		const initialEndDate = new Date();
		initialEndDate.setDate(initialEndDate.getDate() - 10);
		return initialEndDate;
	});

	useEffect(() => {
		if (!discordUser || !guild) return;

		fetch(
			`/api/statistic/${guild.guild_id}/${discordUser.discord_id}/${startDate.toISOString().split("T")[0]}/${endDate.toISOString().split("T")[0]}`,
			{
				method: "GET",
				headers: {
					"Content-Type": "application/json",
				},
				credentials: "include",
			}
		).then(async (response) => {
			if (!response.ok) {
				return;
			}

			if (response.status === 204) {
				setStatistics(null);
				return;
			}

			const data: Statistic[] = await response.json();

			data.forEach(statistic => {
				statistic.online_time = parseTimeStringToSeconds(formatTimeFromMicroseconds(Number(statistic.online_time)));
				statistic.stream_time = parseTimeStringToSeconds(formatTimeFromMicroseconds(Number(statistic.stream_time)));
				statistic.mute_time = parseTimeStringToSeconds(formatTimeFromMicroseconds(Number(statistic.mute_time)));
				statistic.deaf_time = parseTimeStringToSeconds(formatTimeFromMicroseconds(Number(statistic.deaf_time)));
			});

			data.sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime());
			setStatistics(data);
		});
	}, [discordUser, guild, navigate, startDate, endDate]);

	function formatTimeFromMicroseconds(microseconds: number): string {
		const totalSeconds = Math.floor(microseconds / 1_000_000);
		const hours = Math.floor(totalSeconds / 3600);
		const minutes = Math.floor((totalSeconds % 3600) / 60);
		const seconds = totalSeconds % 60;
		return `${String(hours).padStart(2, "0")}:${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
	}

	function parseTimeStringToSeconds(timeString: string): number {
		const [hours, minutes, seconds] = timeString.split(":").map(Number);
		return hours * 3600 + minutes * 60 + seconds;
	}

	function formatSecondsToTime(seconds: number): string {
		const hours = Math.floor(seconds / 3600);
		const minutes = Math.floor((seconds % 3600) / 60);
		const secs = seconds % 60;
		return `${String(hours).padStart(2, "0")}:${String(minutes).padStart(2, "0")}:${String(secs).padStart(2, "0")}`;
	}

	return (
		<div>
			{statistics && statistics.length > 0 ? (
				<ResponsiveContainer width="100%" height={400}>
					<AreaChart data={statistics} margin={{top: 10, right: 30, left: 0, bottom: 0}}>
						<CartesianGrid strokeDasharray="3 3"/>
						<XAxis dataKey="date" tickFormatter={(tick) => new Date(tick).toLocaleDateString()}/>
						<YAxis tickFormatter={(tick) => formatSecondsToTime(Number(tick))}/>
						<Tooltip formatter={(value) => formatSecondsToTime(Number(value))}/>
						<Legend/>
						<Area type="monotone" dataKey="online_time" stroke="#8884d8" fill="#8884d8" name="Online Time"/>
						<Area type="monotone" dataKey="stream_time" stroke="#82ca9d" fill="#82ca9d" name="Stream Time"/>
						<Area type="monotone" dataKey="mute_time" stroke="#ffc658" fill="#ffc658" name="Mute Time"/>
						<Area type="monotone" dataKey="deaf_time" stroke="#ff8042" fill="#ff8042" name="Deaf Time"/>
					</AreaChart>
				</ResponsiveContainer>
			) : (
				<p>Keine Daten verfügbar</p>
			)}
		</div>
	);
}

export default StatisticGraph;
