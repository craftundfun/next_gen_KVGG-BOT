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
import TablePagination from '@mui/material/TablePagination';
import Box from "@mui/material/Box";
import CircularProgress from "@mui/material/CircularProgress";
import TableSortLabel from '@mui/material/TableSortLabel';


export function UserListSite() {
	const {guild} = useGuild();
	const [users, setUsers] = useState<DiscordUser[] | null>(null);
	const [page, setPage] = useState(0);
	const [rowsPerPage, setRowsPerPage] = useState(10);
	const [sortBy, setSortBy] = useState<keyof DiscordUser>("created_at");
	const [orderBy, setOrderBy] = useState<"asc" | "desc">("desc");
	const [count, setCount] = useState(0);

	const handlePageChange = (event: unknown, newPage: number) => {
		setPage(newPage);
	}

	const handleRowsPerPageChange = (event: React.ChangeEvent<HTMLInputElement>) => {
		setRowsPerPage(parseInt(event.target.value, 10));
		setPage(0);
	};

	useEffect(() => {
			if (!guild) return;

			customFetch(`/api/discordUser/all/${guild.guild_id}?orderBy=${orderBy}&sortBy=${sortBy}&start=${rowsPerPage * page}&count=${rowsPerPage}`, {
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
				setCount(data.count);
			})
		},
		[guild, orderBy, page, rowsPerPage, sortBy]
	);

	useEffect(() => {
		console.log("Users:", users);
	}, [users]);

	const getTableHeaderName = (key: string) => {
		switch (key) {
			case "discord_id":
				return "Discord ID";
			case "global_name":
				return "globaler Name";
			case "created_at":
				return "erstellt am";
			default:
				return key;
		}
	}

	return (
		<SiteBlueprint>
			<div>
				{users && users.length > 0 ?
					(
						<div>
							<Paper sx={{width: '100%', mb: 2}}>
								<TableContainer component={Paper}>
									<Table>
										<TableHead sx={{backgroundColor: "primary.main"}}>
											<TableRow>
												{Object.entries(users[0]).map(([key,]) => (
													<TableCell
														key={key}
														align="left"
														sortDirection={sortBy === key ? orderBy : false}
														width={100 / Object.entries(users[0]).length + "%"}
													>
														<TableSortLabel
															active={sortBy === key}
															direction={sortBy === key ? orderBy : 'asc'}
															onClick={() => {
																if (sortBy === key) {
																	setOrderBy(prev => prev === "asc" ? "desc" : "asc");
																} else {
																	setSortBy(key as keyof DiscordUser);
																	setOrderBy("asc");
																}
															}}
														>
															{getTableHeaderName(key)}
														</TableSortLabel>
													</TableCell>
												))}
											</TableRow>
										</TableHead>
										<TableBody sx={{backgroundColor: "secondary.main"}}>
											{users.map((user) => (
												<TableRow
													key={user.discord_id}
													sx={{'&:last-child td, &:last-child th': {border: 0}}}
												>
													{Object.entries(user).map(([key, value]) => (
														<TableCell key={key} align="justify">
															{value}
														</TableCell>
													))}
												</TableRow>
											))}
										</TableBody>
									</Table>
								</TableContainer>
								<Box
									display="flex"
									justifyContent="flex-end"
									sx={{backgroundColor: "primary.main", px: 2}}
								>
									<TablePagination
										rowsPerPageOptions={[10, 15, 20, 25, 50, 100]}
										count={count}
										rowsPerPage={rowsPerPage}
										page={page}
										onPageChange={handlePageChange}
										onRowsPerPageChange={handleRowsPerPageChange}
										component="div"
									/>
								</Box>
							</Paper>
						</div>
					) :
					(
						<div style={{
							display: "flex",
							justifyContent: "center",
							alignItems: "center",
							marginTop: "20rem",
							height: "100%",
							"overflow": "hidden",
						}}>
							<CircularProgress size={100}/>
						</div>
					)
				}
			</div>
		</SiteBlueprint>
	);

}