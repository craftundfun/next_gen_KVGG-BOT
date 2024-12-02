import {useLocation, useNavigate} from "react-router-dom";
import React, {useEffect, useState} from "react";
import apiURL from "../../../modules/ApiUrl";

function LoginRedirect() {
	const location = useLocation();
	const navigate = useNavigate();
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
					navigate("/error");

					return;
				}

				const token = authorizationHeader.split(" ")[1];
				const tokenType = authorizationHeader.split(" ")[0];

				if (token === null) {
					navigate("/error");

					return;
				}

				sessionStorage.setItem('accessToken', token);
				sessionStorage.setItem('tokenType', tokenType);

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
	}, [location, navigate]);

	if (loading) {
		return <p>Loading...</p>;
	}

	return null;
}

export default LoginRedirect;