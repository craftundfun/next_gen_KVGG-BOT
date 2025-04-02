import { useNavigate } from "react-router-dom";
import { useDiscordUser } from "@context/DiscordUserContext";
import { useEffect, useState } from "react";
import { Statistic } from "@customTypes/Statistic";
import React from "react";
import { useGuild } from "@context/GuildContext";
import { Button, Card, CircularProgress, Typography, Menu, MenuItem } from "@mui/material";
import { MoreVert as MoreVertIcon } from "@mui/icons-material";

function Statistics() {
	const navigate = useNavigate();
	const { discordUser } = useDiscordUser();
	const { guild } = useGuild();

	const [statistics, setStatistics] = useState<Statistic | null>(null);
	const [dates, setDates] = useState<Date[] | null>(null);
	const [loadingStatistics, setLoadingStatistics] = useState<boolean>(true);
	const [loadingDates, setLoadingDates] = useState<boolean>(true);
	const [currentDate, setCurrentDate] = useState<Date>(new Date());
	const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
	const open = Boolean(anchorEl);

	const formatter = new Intl.DateTimeFormat('de-DE', {
		day: '2-digit',
		month: '2-digit',
		year: 'numeric'
	});

	// Fetch statistics for the selected date
	useEffect(() => {
		if (!discordUser || !guild) return;

		const formattedDate = (
			`${currentDate.getFullYear()}-${(currentDate.getMonth() + 1).toString().padStart(2, '0')}-${currentDate.getDate().toString().padStart(2, '0')}`
		);

		fetch(`/api/statistic/${guild.guild_id}/${discordUser.discord_id}/${formattedDate}`, {
			method: "GET",
			headers: {
				"Content-Type": "application/json",
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
	}, [navigate, discordUser, guild, currentDate]);

	// Fetch all available dates for the user
	useEffect(() => {
		if (!discordUser || !guild) return;

		setLoadingDates(true);

		fetch(`/api/statistic/${guild.guild_id}/${discordUser.discord_id}/dates`, {
			method: "GET",
			headers: {
				"Content-Type": "application/json",
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
			const datesSet = new Set(datesFromApi.map((date: { getTime: () => never; }) => date.getTime()));
			const current = new Date(minDate);

			// Insert all missing dates between the first date and today
			while (current <= today) {
				if (!datesSet.has(current.getTime())) {
					datesFromApi.push(new Date(current));
					datesSet.add(current.getTime());
				}

				current.setDate(current.getDate() + 1);
			}

			setDates(datesFromApi.sort((a: Date, b: Date) => b.getTime() - a.getTime()));
			setLoadingDates(false);
		})
	}, [discordUser, guild, navigate]);

	const handleMenuClick = (event: React.MouseEvent<HTMLElement>) => {
		setAnchorEl(event.currentTarget);
	};

	const handleMenuClose = () => {
		setAnchorEl(null);
	};

	const handleDateChange = (date: Date) => {
		setCurrentDate(date);
		setAnchorEl(null);
	};

	return (
		<div className="flex flex-col items-center p-6 text-white bg-gray-900 rounded-lg shadow-md w-full max-w-4xl mx-auto">
			<div className="flex items-center space-x-6">
				<Typography variant="h5" className="font-bold">
					Statistiken (nur Datendisplay)
				</Typography>
				<Button
					variant="contained"
					color="primary"
					onClick={handleMenuClick}
					endIcon={<MoreVertIcon />}
				>
					Aktuelles Datum: {formatter.format(currentDate)}
				</Button>
				<Menu
					anchorEl={anchorEl}
					open={open}
					onClose={handleMenuClose}
				>
					{loadingDates ? (
						<CircularProgress size={24} />
					) : dates ? (
						dates.map((date, index) => (
							<MenuItem key={index} onClick={() => handleDateChange(date)}>
								{formatter.format(date)}
							</MenuItem>
						))
					) : (
						<MenuItem disabled>Keine Daten verfügbar</MenuItem>
					)}
				</Menu>
			</div>

			<Card className="bg-gray-800 p-4 rounded-lg shadow w-full mt-4">
				<Typography variant="body2">
					Discord ID: <span className="font-semibold">{discordUser?.discord_id}</span>
				</Typography>
				<Typography variant="body2">
					Global Name: <span className="font-semibold">{discordUser?.global_name}</span>
				</Typography>
				<Typography variant="body2">
					Created At: <span className="font-semibold">{discordUser?.created_at}</span>
				</Typography>
			</Card>

			<Typography variant="h6" className="text-xl font-semibold mt-6">
				Statistics
			</Typography>
			<Card className="bg-gray-800 p-4 rounded-lg shadow w-full mt-4">
				{loadingStatistics ? (
					<CircularProgress size={24} />
				) : statistics ? (
					<>
						<Typography variant="body2">Date: {statistics.date}</Typography>
						<Typography variant="body2">Online Time: {statistics?.online_time}</Typography>
						<Typography variant="body2">Stream Time: {statistics?.stream_time}</Typography>
						<Typography variant="body2">Mute Time: {statistics?.mute_time}</Typography>
						<Typography variant="body2">Deaf Time: {statistics?.deaf_time}</Typography>
						<Typography variant="body2">Message Count: {statistics?.message_count}</Typography>
						<Typography variant="body2">Command Count: {statistics?.command_count}</Typography>
					</>
				) : (
					<Typography variant="body2" className="text-center text-gray-500 mt-6">
						Keine Statistiken verfügbar
					</Typography>
				)}
			</Card>
		</div>
	);
}

export default Statistics;
