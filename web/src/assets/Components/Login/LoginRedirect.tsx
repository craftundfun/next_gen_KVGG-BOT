import {useLocation, useNavigate} from "react-router-dom";
import React, {useEffect, useRef, useState} from "react";
import apiURL from "../../../modules/ApiUrl";
import {useAuth} from "../../../modules/AuthContext";
import BaseLayout from "../ui/base";
import {Spinner} from "../ui/spinner";

function LoginRedirect() {
	const location = useLocation();
	const navigate = useNavigate();
	const {login} = useAuth();
	const [loading, setLoading] = useState(true);
	const hasFetched = useRef(false);

	useEffect(() => {
		// only call the backend once here, otherwise we might reauthenticate the user and this will fail
		if (hasFetched.current) return;
		hasFetched.current = true;

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
					console.log("Error: No authorization header");

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
		}).finally(() => {
			setLoading(false);
		});
	}, [login, location, navigate]);

	if (loading) {
		return (
			<BaseLayout>
				<div style={{
					display: 'flex',
					justifyContent: 'center',
					alignItems: 'center',
					height: '100vh',
				}}>
					<Spinner size="large"/>
				</div>
			</BaseLayout>
		);
	}

	return null;
}

export default LoginRedirect;