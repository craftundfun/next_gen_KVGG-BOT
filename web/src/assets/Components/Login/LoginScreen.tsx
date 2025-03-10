import * as React from "react";
import {useAuth} from "@modules/AuthContext";
import {Card, CardContent, CardHeader, CardTitle} from "@ui/card";
import {Avatar, AvatarFallback, AvatarImage} from "@ui/avatar";
import {discordOAuthUrlDevelopment, copyrightUrl, backendUrl, discordOAuthUrlProduction} from "@modules/Constants";
import {useEffect} from "react";
import {DiscordUser} from "@customTypes/DiscordUser";
import {parseWebsiteUser, WebsiteUser} from "@customTypes/WebsiteUser";
import {useNavigate} from "react-router-dom";
import {useDiscordUser} from "@context/DiscordUserContext";
import {useWebsiteUser} from "@context/WebsiteUserContext";
import {Button} from "@ui/button";

function LoginScreen() {
	const {remindMe, setRemindMe, login} = useAuth();
	const navigate = useNavigate();
	const {setDiscordUser} = useDiscordUser();
	const {setWebsiteUser} = useWebsiteUser();

	const handleLogin = () => {
		if (process.env.NODE_ENV !== "production") {
			window.open(discordOAuthUrlDevelopment, "_parent");
		} else {
			window.open(discordOAuthUrlProduction, "_parent");
		}
	};

	useEffect(() => {
		fetch(backendUrl + "/auth/remindMeLogin", {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json',
			},
			credentials: 'include',
		}).then((response) => {
			if (!response.ok) {
				return;
			}

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
		});
	}, [login, navigate, setDiscordUser, setWebsiteUser]);

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
								erinnern
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