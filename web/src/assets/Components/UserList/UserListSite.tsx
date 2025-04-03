import React, {useEffect, useState} from "react";
import SiteBlueprint from "@modules/SiteBlueprint";
import {customFetch} from "@modules/CustomFetch";
import {DiscordUser} from "@customTypes/DiscordUser";
import {useGuild} from "@context/GuildContext";
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import {CircularProgress} from "@mui/material";


export function UserListSite() {
	const {guild} = useGuild();
	const [users, setUsers] = useState<DiscordUser[] | null>(null);
	const start = 0;
	const count = 10;
	const orderBy = "created_at";
	const sortBy = "desc";

	useEffect(() => {
			if (!guild) return;

			customFetch(`/api/discordUser/all/${guild.guild_id}?start=${start}&count=${count}&orderBy=${orderBy}&sortBy=${sortBy}`, {
				method: "GET",
				headers: {
					"Content-Type": "application/json",
				},
				credentials: "include",
			}).then(async response => {
				if (!response.ok) {
					console.error("Error fetching users:", response);

					return;
				}

				const data = await response.json();
				setUsers(data.discordUsers);
			})
		},
		[guild]
	);

	return (
		<SiteBlueprint>
			<div>
				{users ?
					(
						<TableContainer component={Paper}>
							<Table>
								<TableHead sx={{backgroundColor: "primary.main"}}>
									<TableRow>
										<TableCell align="justify" variant="head">
											User
										</TableCell>
										<TableCell align="justify" variant="head">
											Created at
										</TableCell>
									</TableRow>
								</TableHead>
								<TableBody sx={{backgroundColor: "secondary.main"}}>
									{users.map((user) => (
										<TableRow
											key={user.discord_id}
											sx={{'&:last-child td, &:last-child th': {border: 0}}}
										>
											<TableCell component="th" scope="row" align="justify">
												{user.global_name}
											</TableCell>
											<TableCell align="justify">{user.created_at}</TableCell>
										</TableRow>
									))}
								</TableBody>
							</Table>
						</TableContainer>
					) :
					(
						<CircularProgress size={24}/>
					)
				}
			</div>
		</SiteBlueprint>
	);

}