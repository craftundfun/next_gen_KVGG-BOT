import React from 'react';
import {useEffect, useState} from 'react';
import {useNavigate} from "react-router-dom";
import {backendUrl} from "@modules/Constants";
import BaseLayout from "@ui/SiteBlueprint";
import PersonalDashboard from "@components/Dashboard/PersonalInfo/PersonalDashboard";

function Dashboard() {
	const navigate = useNavigate();

	const token = sessionStorage.getItem('jwt');
	const tokenType = sessionStorage.getItem('tokenType');

	const [users, setUsers] = useState<string | null>(null);
	const [guilds, setGuilds] = useState<string | null>(null);
	const [loading, setLoading] = useState<boolean>(true);

//	useEffect(() => {
//		// Get all users
//		fetch(backendUrl + "/api/discordUser/all", {
//			method: 'GET',
//			headers: {
//				'Content-Type': 'application/json',
//				'Authorization': tokenType + ' ' + token,
//			},
//			credentials: 'include',
//		}).then((response) => {
//			if (!response.ok) {
//				navigate("/error");
//
//				return null;
//			}
//
//			return response.json();
//		}).then((data) => {
//			if (data) {
//				setUsers(JSON.stringify(data));
//				//setLoading(false);
//			}
//		}).catch((error) => {
//			console.log(error);
//
//			navigate("/error");
//
//			return null;
//		});
//
//		fetch(backendUrl + "/api/guild/all", {
//			method: 'GET',
//			headers: {
//				'Content-Type': 'application/json',
//				'Authorization': tokenType + ' ' + token,
//			},
//			credentials: 'include',
//		}).then((response) => {
//			if (!response.ok) {
//				navigate("/error");
//
//				return null;
//			}
//
//			return response.json();
//		}).then((data) => {
//			if (data) {
//				setGuilds(JSON.stringify(data));
//				setLoading(false);
//			}
//		}).catch((error) => {
//			console.log(error);
//
//			navigate("/error");
//
//			return null;
//		});
//	}, [navigate, token, tokenType]);

	return (
		<div>
			<BaseLayout>
				{(
					<div className=" flex-grow grid grid-cols-2 grid-rows-2 h-full">
						<div className="overflow-auto">
							<p>Test</p>
						</div>
						<div className="overflow-auto">
							<p>Test</p>
						</div>
						<div className="overflow-auto">
							<p>Test</p>
						</div>
						<div className="overflow-auto">
							<PersonalDashboard/>
						</div>
					</div>
				)}
			</BaseLayout>
		</div>
	);
}

export default Dashboard;