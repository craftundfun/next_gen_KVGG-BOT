import {useLocation, useNavigate} from "react-router-dom";
import React, {useEffect, useRef, useState} from "react";
import apiURL from "../../../modules/ApiUrl";
import {useAuth} from "../../../modules/AuthContext";
import {Spinner} from "../ui/spinner";
import {useDiscordUser} from "../../../context/DiscordUserContext";
import {useWebsiteUser} from "../../../context/WebsiteUserContext";
import parseDiscordUser from "../../../types/DiscordUser";
import parseWebsiteUser from "../../../types/WebsiteUser";
import BaseLayout from "../ui/SiteBlueprint";

function LoginRedirect() {
	const location = useLocation();
	const navigate = useNavigate();
	const {login} = useAuth();
	const {setDiscordUser, discordUser} = useDiscordUser();
	const {setWebsiteUser, websiteUser} = useWebsiteUser();
	const [loading, setLoading] = useState(true);
	const hasFetched = useRef(false);

	useEffect(() => {
		// only call the backend once here, otherwise we might reauthenticate the user, and this will fail
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
				const discordIdHeader = response.headers.get("DiscordId");

				if (authorizationHeader === null) {
					console.log("Error: No authorization header");

					return;
				} else if (discordIdHeader === null) {
					console.log("Error: No discord id header");

					return;
				}

				const token = authorizationHeader.split(" ")[1];
				const tokenType = authorizationHeader.split(" ")[0];

				sessionStorage.setItem('tokenType', tokenType);
				login(token);

				fetch(apiURL + `/api/discordUser/${discordIdHeader}`, {
					method: 'GET',
					headers: {
						'Content-Type': 'application/json',
						'Authorization': tokenType + ' ' + token,
					},
					credentials: 'include',
				}).then(async response => {
					if (!response.ok) {
						console.log("Error: Could not fetch discord user");

						navigate("/error");

						return;
					}

					let discordUserFromRequest = parseDiscordUser(await response.json());

					if (discordUserFromRequest === null) {
						console.log("Error: Could not parse discord user");

						navigate("/error");

						return;
					}

					setDiscordUser(discordUserFromRequest);
				}).catch((error) => {
					console.log(error);

					navigate("/error");

					return;
				});

				fetch(apiURL + `/api/websiteUser/${discordIdHeader}`, {
					method: 'GET',
					headers: {
						'Content-Type': 'application/json',
						'Authorization': tokenType + ' ' + token,
					},
					credentials: 'include',
				}).then(async response => {
					if (!response.ok) {
						console.log("Error: Could not fetch website user");

						navigate("/error");

						return;
					}

					let websiteUserFromRequest = parseWebsiteUser(await response.json());

					if (websiteUserFromRequest === null) {
						console.log("Error: Could not parse website user");

						navigate("/error");

						return;
					}

					setWebsiteUser(websiteUserFromRequest);
				})

				navigate("/dashboard");
			} else {
				navigate("/error");

				return;
			}
		}).catch((error) => {
			console.log(error);

			navigate("/error");

			return;
		}).finally(() => {
			setLoading(false);
		});
	}, [login, location, navigate, setDiscordUser, discordUser, setWebsiteUser, websiteUser]);

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