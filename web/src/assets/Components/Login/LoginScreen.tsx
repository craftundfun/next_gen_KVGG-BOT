import * as React from "react";
import {useEffect, useState} from "react";
import {useNavigate} from "react-router-dom";
import Button from "@mui/material/Button";
import Card from "@mui/material/Card";
import CardHeader from "@mui/material/CardHeader";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";
import Avatar from "@mui/material/Avatar";
import Checkbox from "@mui/material/Checkbox";
import FormControlLabel from "@mui/material/FormControlLabel";

function LoginScreen() {
	const navigate = useNavigate();
	const [remindMe, setRemindMe] = useState<boolean>(false);

	const handleLogin = () => {
		const redirectUri = process.env.REACT_APP_DISCORD_OAUTH_URL;

		window.open(redirectUri + "&state=remindMe=" + remindMe.toString().toLowerCase(), "_parent");
	};

	// upon loading the site, check if the user has a refresh token and log in immediately
	useEffect(() => {
		fetch("api/welcomeBack", {
			method: "GET",
			credentials: "include",
		}).then((response) => {
			if (response.status !== 200) {
				return;
			}

			navigate("/dashboard");
		});
	}, [navigate]);

	return (
		<div
			className="flex flex-col justify-between h-screen bg-gradient-to-b from-gray-900 to-gray-800 overflow-hidden">
			<div className="flex items-center justify-center h-full p-4">
				<Card
					className="flex flex-col items-center justify-center w-full max-w-md p-6 shadow-xl overflow-hidden"
					sx={{
						maxWidth: 800,
						outline: "solid 1px #4B5563",
						borderRadius: "8px",
						backgroundColor: "transparent",
					}}
				>
					<CardHeader
						className="flex flex-col items-center space-y-2"
						sx={{
							display: "flex",
							flexDirection: "column",
							alignItems: "center",
							justifyContent: "center",
							textAlign: "center",
						}}
						avatar={
							<Avatar
								alt="Discord"
								src="/KVGG/KVGG Logo Icon.png"
								sx={{width: 64, height: 64, align: "center", marginLeft: 2}}
							/>
						}
						title={
							<Typography variant="h5" color="white" sx={{fontWeight: 600}}>
								KVGG
							</Typography>
						}
					/>
					<Typography variant="h4" color="primary" align="center" sx={{mt: 2, fontWeight: 700}}>
						Login mit Discord
					</Typography>
					<CardContent className="flex flex-col items-center mt-6 space-y-6">
						<Typography variant="body1" color="white" align="center" sx={{lineHeight: 1.5}}>
							Melde dich mit deinem Discord-Account an, um Zugriff auf unsere Plattform zu erhalten.
						</Typography>
						<Button
							onClick={handleLogin}
							variant="contained"
							color="primary"
							sx={{width: "100%", py: 2, fontWeight: 600, fontSize: "1.1rem"}}
						>
							Login mit Discord
						</Button>
						<div className="flex items-center space-x-2">
							<FormControlLabel
								control={
									<Checkbox
										checked={remindMe}
										onChange={() => setRemindMe(!remindMe)}
										color="default"
									/>
								}
								label={
									<Typography variant="body2" color="white">
										Erinnern für 14 Tage?
									</Typography>
								}
							/>
						</div>
					</CardContent>
				</Card>
			</div>
			<div className="p-4">
				<Typography variant="body2" color="white" align="center" sx={{fontSize: "0.875rem"}}>
					© 2025{" "}
					<a href="https://github.com/craftundfun" className="underline text-accent">
						craftundfun
					</a>
					. All rights reserved.
				</Typography>
			</div>
		</div>
	);
}

export default LoginScreen;
