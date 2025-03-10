import {useLocation, useNavigate} from "react-router-dom";
import React, {useEffect, useRef, useState} from "react";
import {backendUrl} from "@modules/Constants";
import {useAuth} from "@modules/AuthContext";
import {Spinner} from "@ui/spinner";
import {useDiscordUser} from "@context/DiscordUserContext";
import {useWebsiteUser} from "@context/WebsiteUserContext";
import {parseWebsiteUser, WebsiteUser} from "@customTypes/WebsiteUser";
import {DiscordUser} from "@customTypes/DiscordUser";
import BaseLayout from "@ui/SiteBlueprint";


function Login() {
	const location = useLocation();
	const navigate = useNavigate();
	const {login, remindMe} = useAuth();
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

		console.log(remindMe);

		fetch(backendUrl + "/auth/discord?code=" + code + "&remindMe=" + remindMe.toString(), {
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

				const tokenType = authorizationHeader.split(" ")[0];
				const token = authorizationHeader.split(" ")[1];

				sessionStorage.setItem('tokenType', tokenType);
				login(token);

				fetch(backendUrl + `/api/discordUser/${discordIdHeader}`, {
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

					const discordUserFromRequest: DiscordUser | null = await response.json();

					if (discordUserFromRequest === null) {
						console.log("Error: Could not parse discord user");

						navigate("/error");

						return;
					}

					console.log(discordUserFromRequest);

					setDiscordUser(discordUserFromRequest);
				}).catch((error) => {
					console.log(error);

					navigate("/error");

					return;
				});

				fetch(backendUrl + `/api/websiteUser/${discordIdHeader}`, {
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

					const websiteUserFromRequest: WebsiteUser | null = parseWebsiteUser(await response.json());

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
	}, [login, location, navigate, setDiscordUser, discordUser, setWebsiteUser, websiteUser, remindMe]);

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

export default Login;