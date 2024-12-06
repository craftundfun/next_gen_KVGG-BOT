import * as React from 'react';
import {useEffect, useState} from 'react';
import {useNavigate} from "react-router-dom";
import apiURL from "../../../modules/ApiUrl";
import BaseLayout from "@/assets/Components/ui/SiteBlueprint";

function Dashboard() {
	const navigate = useNavigate();

	const token = sessionStorage.getItem('jwt');
	const tokenType = sessionStorage.getItem('tokenType');

	let [users, setUsers] = useState<string | null>(null);
	let [guilds, setGuilds] = useState<string | null>(null);
	let [loading, setLoading] = useState<boolean>(true);

	useEffect(() => {
		// Get all users
		fetch(apiURL + "/api/discordUser/all", {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json',
				'Authorization': tokenType + ' ' + token,
			},
			credentials: 'include',
		}).then((response) => {
			if (!response.ok) {
				navigate("/error");

				return null;
			}

			return response.json();
		}).then((data) => {
			if (data) {
				setUsers(JSON.stringify(data));
				//setLoading(false);
			}
		}).catch((error) => {
			console.log(error);

			navigate("/error");

			return null;
		});

		fetch(apiURL + "/api/guild/all", {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json',
				'Authorization': tokenType + ' ' + token,
			},
			credentials: 'include',
		}).then((response) => {
			if (!response.ok) {
				navigate("/error");

				return null;
			}

			return response.json();
		}).then((data) => {
			if (data) {
				setGuilds(JSON.stringify(data));
				setLoading(false);
			}
		}).catch((error) => {
			console.log(error);

			navigate("/error");

			return null;
		});
	}, [navigate, token, tokenType]);

	return (
		<div>
			<BaseLayout>
				{loading ? (
					<p>Loading...</p>
				) : (
					<>
						<p>{tokenType} {token}</p>
						<p>{users}</p>
						<p>{guilds}</p>
					</>
				)}
			</BaseLayout>
		</div>
	);
}

export default Dashboard;