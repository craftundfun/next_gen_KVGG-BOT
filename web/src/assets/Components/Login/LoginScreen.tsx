import * as React from "react";
import {useAuth} from "@modules/AuthContext";
import {Card, CardContent, CardHeader, CardTitle} from "@ui/card";
import {Avatar, AvatarFallback, AvatarImage} from "@ui/avatar";
import {copyrightUrl, discordOAuthUrl} from "@modules/Constants";
import {useEffect} from "react";
import {useNavigate} from "react-router-dom";
import {useDiscordUser} from "@context/DiscordUserContext";
import {useWebsiteUser} from "@context/WebsiteUserContext";
import {Button} from "@ui/button";
import getLoginData from "@components/Login/getLoginData";
import {useGuild} from "@context/GuildContext";

function LoginScreen() {
	const {remindMe, setRemindMe, login} = useAuth();
	const navigate = useNavigate();
	const {setDiscordUser} = useDiscordUser();
	const {setWebsiteUser} = useWebsiteUser();
	const {setGuild} = useGuild();

	const handleLogin = () => {
		// redirect to the discord oauth2 login page
		window.open(discordOAuthUrl, "_parent");
	};

	// upon loading the site, check if the user has a refresh token and log in immediately
	useEffect(() => {
		fetch("/auth/login", {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json',
			},
			credentials: 'include',
		}).then((response) => {
			// if the response was not ok, the user had no refresh token or something is missing
			if (!response.ok) {
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
	}, [login, navigate, setDiscordUser, setGuild, setWebsiteUser]);

	return (
		<div className="flex flex-col justify-between h-screen bg-gradient-to-b from-gray-900 to-gray-800">
			<div className="flex items-center justify-center h-full">
				<Card
					className="flex flex-col items-center justify-center w-1/3 max-w-full max-h-full p-6 shadow-xl overflow-hidden">
					<CardHeader className="flex flex-col items-center space-y-2">
						<Avatar className="w-16 h-16">
							<AvatarImage src="/KVGG/KVGG Logo Icon.png"/>
							<AvatarFallback>Discord</AvatarFallback>
						</Avatar>
						<p className="text-white text-xl">KVGG</p>
					</CardHeader>
					<CardTitle className="text-primary text-2xl text-center">
						Login mit Discord
					</CardTitle>
					<CardContent className="flex flex-col items-center mt-8 space-y-4">
						<p className="text-gray-400 text-center">
							Melde dich mit deinem Discord-Account an, um Zugriff auf unsere Plattform zu erhalten.
						</p>
						<Button
							onClick={handleLogin}
							className="bg-primary hover:bg-secondary text-white px-4 py-2 rounded-lg w-full"
						>
							Login mit Discord
						</Button>
						<div className="flex items-center space-x-2">
							<input
								type="checkbox"
								id="remindMe"
								checked={remindMe}
								onChange={() => setRemindMe(!remindMe)}
								className="w-4 h-4"
							/>
							<label htmlFor="remindMe" className="text-gray-400 text-sm">
								erinnern für 14 Tage?
							</label>
						</div>
					</CardContent>
				</Card>
			</div>
			<div>
				<p className="text-white text-center">
					© 2025 <a href={copyrightUrl} className="underline text-accent">craftundfun</a>.
					All rights reserved.
				</p>
			</div>
		</div>
	);
}

export default LoginScreen;