import {useLocation, useNavigate} from "react-router-dom";
import React, {useEffect, useState} from "react";
import apiURL from "../../../modules/ApiUrl";
import {useAuth} from "../../../modules/AuthContext";

function LoginRedirect() {
	/*
	Discord OAuth2 reroutes the user to this page after successful login. The page then extracts the code from the URL
	and sends it to the backend to receive a JWT token. The token is then stored in the session storage and the user is
	redirected to the dashboard.
	 */
	const location = useLocation();
	const navigate = useNavigate();
	const {login} = useAuth();

	const [loading, setLoading] = useState(true);

	useEffect(() => {
		const params = new URLSearchParams(location.search);
		const code = params.get("code");

		if (code === null) {
			navigate("/error");

			return;
		}

		fetch(apiURL + "/auth/discord?code=" + code, {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json',
			},
			credentials: 'include',
		}).then((response) => {
			if (response.ok) {
				const authorizationHeader = response.headers.get("Authorization");

				if (authorizationHeader === null) {
					return;
				}

				const token = authorizationHeader.split(" ")[1];
				const tokenType = authorizationHeader.split(" ")[0];

				sessionStorage.setItem('tokenType', tokenType);
				login(token);

				navigate("/dashboard");
			} else {
				navigate("/error");
			}
		}).catch((error) => {
			console.log(error);

			navigate("/error");

			return;
		}).finally(() => {
			setLoading(false);
		});
	}, [login, location, navigate]);

	if (loading) {
		return <p>Loading...</p>;
	}

	return null;
}

export default LoginRedirect;