import {useLocation, useNavigate} from "react-router-dom";
import React, {useEffect, useRef} from "react";
import {backendUrl} from "@modules/Constants";
import {useAuth} from "@context/AuthContext";
import {Spinner} from "@ui/spinner";
import {useDiscordUser} from "@context/DiscordUserContext";
import {useWebsiteUser} from "@context/WebsiteUserContext";
import BaseLayout from "@ui/SiteBlueprint";
import getLoginData from "@components/Login/getLoginData";
import {useGuild} from "@context/GuildContext";


function Login() {
	const location = useLocation();
	const navigate = useNavigate();
	const hasFetched = useRef(false);

	const {login, remindMe} = useAuth();
	const {setDiscordUser} = useDiscordUser();
	const {setWebsiteUser} = useWebsiteUser();
	const {setGuild} = useGuild();

	useEffect(() => {
		// only call the backend once here, otherwise we might reauthenticate the user, and this will fail
		if (hasFetched.current) {
			return;
		}

		hasFetched.current = true;

		const params = new URLSearchParams(location.search);
		const code = params.get("code");

		if (code === null) {
			navigate("/error");

			return;
		}

		fetch(backendUrl + "/auth/newLogin?code=" + code + "&remindMe=" + remindMe.toString(), {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json',
			},
			credentials: 'include',
		}).then((response) => {
			if (!response.ok) {
				navigate("/error");

				return;
			}

			const loginData = getLoginData(response);

			if (!loginData) {
				navigate("/error");

				return;
			}

			setDiscordUser(loginData[2]);
			setWebsiteUser(loginData[3]);
			login(loginData[1]);
			sessionStorage.setItem("tokenType", loginData[0]);
			setGuild(loginData[4]);

			navigate("/dashboard");
		});
	}, [location.search, login, navigate, remindMe, setDiscordUser, setGuild, setWebsiteUser]);

	return (
		<BaseLayout>
			<div style={{
				display: 'flex',
				justifyContent: 'center',
				alignItems: 'center',
				minHeight: '100vh',
				overflow: 'hidden'
			}}>
				<Spinner size="large"/>
			</div>
		</BaseLayout>
	);
}

export default Login;