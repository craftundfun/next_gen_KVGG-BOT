import React, {useEffect} from 'react';
import BaseLayout from "@ui/SiteBlueprint";
import Statistics from "@components/Dashboard/PersonalInfo/Statistics";
import StatisticGraph from "@components/Dashboard/PersonalInfo/StatisticGraph";
import {useAuth} from "@context/AuthContext";
import {useNavigate} from "react-router-dom";

function Dashboard() {
	const navigate = useNavigate();
	const {login, logout} = useAuth();

	useEffect(() => {
		fetch("/auth/loggedIn", {
			method: "GET",
			credentials: "include"
		}).then(response => {
			console.log(response);

			if (response.status !== 200) {
				logout();
				navigate("/forbidden");

				return;
			}

			login();
		});
	}, [login, logout, navigate]);


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
							<StatisticGraph/>
						</div>
						<div className="overflow-auto">
							<Statistics/>
						</div>
					</div>
				)}
			</BaseLayout>
		</div>
	);
}

export default Dashboard;