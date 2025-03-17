import {useNavigate} from "react-router-dom";
import {useDiscordUser} from "@context/DiscordUserContext";
import {useEffect, useState} from "react";
import {Statistic} from "@customTypes/Statistic";
import React from "react";
import {useGuild} from "@context/GuildContext";
import {Spinner} from "@ui/spinner";
import {
	DropdownMenu,
	DropdownMenuContent,
	DropdownMenuGroup,
	DropdownMenuItem,
	DropdownMenuTrigger,
} from "@ui/dropdown-menu";

function Statistics() {
	const navigate = useNavigate();
	const token = sessionStorage.getItem('jwt');
	const tokenType = sessionStorage.getItem('tokenType');
	const {discordUser} = useDiscordUser();
	const {guild} = useGuild();

	const [statistics, setStatistics] = useState<Statistic | null>(null);
	const [dates, setDates] = useState<Date[] | null>(null);
	const [loadingStatistics, setLoadingStatistics] = useState<boolean>(true);
	const [loadingDates, setLoadingDates] = useState<boolean>(true);
	const [currentDate, setCurrentDate] = useState<Date>(new Date());

	const formatter = new Intl.DateTimeFormat('de-DE', {
		day: '2-digit',
		month: '2-digit',
		year: 'numeric'
	});

	// fetch statistics for the selected date
	useEffect(() => {
		if (!discordUser || !guild) return;

		const formattedDate = currentDate.toISOString().split('T')[0];

		fetch(`/api/statistic/${guild.guild_id}/${discordUser.discord_id}/${formattedDate}`, {
			method: "GET",
			headers: {
				"Content-Type": "application/json",
				Authorization: `${tokenType} ${token}`,
			},
			credentials: "include",
		}).then(async response => {
			if (!response.ok) {
				navigate("/error");

				return;
			}

			if (response.status === 204) {
				setStatistics(null);
				setLoadingStatistics(false);

				return;
			}

			setStatistics(await response.json());
			setLoadingStatistics(false);
		})
	}, [navigate, token, tokenType, discordUser, guild, currentDate]);

	// fetch all available dates for the user
	useEffect(() => {
		if (!discordUser || !guild) return;

		setLoadingDates(true);

		fetch(`/api/statistic/${guild.guild_id}/${discordUser.discord_id}/dates`, {
			method: "GET",
			headers: {
				"Content-Type": "application/json",
				Authorization: `${tokenType} ${token}`,
			},
			credentials: "include",
		}).then(async response => {
			if (!response.ok) {
				navigate("/error");

				return;
			}

			if (response.status === 204) {
				setDates(null);
				setLoadingDates(false);

				return;
			}

			let datesFromApi = await response.json();
			const today = new Date();
			datesFromApi = datesFromApi.map((date: string) => new Date(date));
			const minDate = new Date(Math.min(...datesFromApi.map((date: Date) => date.getTime())));

			for (let i = 0; i < (today.getTime() - minDate.getTime() * 24 * 60 * 60 * 1000); i += 1) {
				const date = new Date(minDate.getTime() + i * 24 * 60 * 60 * 1000);
				if (!datesFromApi.some((d: Date) => d.getTime() === date.getTime())) {
					datesFromApi.push(date);
				}
			}

			datesFromApi.push(today);
			setDates(datesFromApi.sort((a: Date, b: Date) => b.getTime() - a.getTime()));
			setLoadingDates(false);
		})
	}, [discordUser, guild, navigate, token, tokenType]);

	return (
		<div
			className="flex flex-col items-center p-6 text-white bg-gray-900 rounded-lg shadow-md w-full max-w-4xl mx-auto">
			<>
				<div className="flex items-center space-x-6">
					<h1 className="text-2xl font-bold">Statistiken (nur Datendisplay)</h1>
					<DropdownMenu>
						<DropdownMenuTrigger
							className="btn bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded h-10 flex items-center"
						>
							Aktuelles Datum: {formatter.format(currentDate)}
						</DropdownMenuTrigger>
						<DropdownMenuContent
							className="bg-gray-800 text-white mt-2 rounded shadow-lg max-h-60 overflow-auto w-48"
						>
							{loadingDates ? (
								<Spinner/>
							) : dates ? (
								<DropdownMenuGroup>
									{dates.map((date) => (
										<DropdownMenuItem
											key={date.toString()}
											onClick={() => setCurrentDate(date)}
											className="cursor-pointer px-4 py-2 hover:bg-gray-700"
										>
											{formatter.format(date)}
										</DropdownMenuItem>
									))}
								</DropdownMenuGroup>
							) : (
								<p className="text-center text-gray-500">Keine (weiteren) Daten verfügbar</p>
							)}
						</DropdownMenuContent>
					</DropdownMenu>
				</div>

				<div className="bg-gray-800 p-4 rounded-lg shadow w-full mt-4">
					<p className="text-sm">Discord ID: <span
						className="font-semibold">{discordUser?.discord_id}</span></p>
					<p className="text-sm">Global Name: <span
						className="font-semibold">{discordUser?.global_name}</span></p>
					<p className="text-sm">Created At: <span
						className="font-semibold">{discordUser?.created_at}</span></p>
				</div>


				<h2 className="text-xl font-semibold mt-6">Statistics</h2>
				<div className="bg-gray-800 p-4 rounded-lg shadow w-full">
					{loadingStatistics ? (
						<Spinner/>
					) : (
						statistics ? (
							<>
								<p>Date: {statistics.date}</p>
								<p>Online Time: {statistics?.online_time}</p>
								<p>Stream Time: {statistics?.stream_time}</p>
								<p>Mute Time: {statistics?.mute_time}</p>
								<p>Deaf Time: {statistics?.deaf_time}</p>
								<p>Message Count: {statistics?.message_count}</p>
								<p>Command Count: {statistics?.command_count}</p>
							</>
						) : (
							<p className="text-center text-gray-500 mt-6">Keine Statistiken verfügbar</p>
						)
					)}
				</div>
			</>
		</div>
	);
}

export default Statistics;
