import * as React from 'react';
import {useEffect, useState} from 'react';
import {useNavigate} from "react-router-dom";
import apiURL from "../../../modules/ApiUrl";

function Dashboard() {
	const navigate = useNavigate();

	const token = sessionStorage.getItem('jwt');
	const tokenType = sessionStorage.getItem('tokenType');

	let [user, setUser] = useState<string | null>(null);
	let [loading, setLoading] = useState<boolean>(true);

	useEffect(() => {
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
				setUser(JSON.stringify(data));
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
			<h1>Dashboard</h1>
			{loading ? (
				<p>Loading...</p>
			) : (
				<>
					<p>{tokenType} {token}</p>
					<p>{user}</p>
				</>
			)}
		</div>
	);
}

export default Dashboard;