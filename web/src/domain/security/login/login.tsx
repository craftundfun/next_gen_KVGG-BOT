import * as React from "react";
import {useState} from "react";
import Avatar from "@mui/material/Avatar";
import Button from "@mui/material/Button";
import Checkbox from "@mui/material/Checkbox";
import Typography from "@mui/material/Typography";
import FormControlLabel from "@mui/material/FormControlLabel";
import Paper from "@mui/material/Paper";
import Box from "@mui/material/Box";
import Copyright from "../../common/component/copyright.tsx";

function Login(): React.ReactNode {
	const [remindMe, setRemindMe] = useState<boolean>(false);

	const handleLogin = () => {
		const redirectUri = import.meta.env.VITE_DISCORD_OAUTH_URL;
		window.open(
			redirectUri + "&state=remindMe=" + remindMe.toString().toLowerCase(),
			"_parent"
		);
	};

	return (
		<Box
			sx={{
				minHeight: "100dvh",
				minWidth: "100dvw",
				background: "linear-gradient(135deg, #232526 0%, #414345 100%)",
				display: "flex",
				flexDirection: "column",
				justifyContent: "space-between",
			}}
		>
			<Box sx={{flex: 1, display: "flex", alignItems: "center", justifyContent: "center"}}>
				<Paper
					elevation={8}
					sx={{
						p: 5,
						borderRadius: 4,
						minWidth: 350,
						maxWidth: 400,
						background: "rgba(30, 41, 59, 0.95)",
						boxShadow: "0 8px 32px 0 rgba(31, 38, 135, 0.37)",
						backdropFilter: "blur(6px)",
						border: "1px solid rgba(255,255,255,0.08)",
						display: "flex",
						flexDirection: "column",
						alignItems: "center",
					}}
				>
					<Avatar
						alt="Discord"
						src="/KVGG/KVGG Logo Icon.png"
						sx={{
							width: 72,
							height: 72,
							mb: 2,
							bgcolor: "#5865F2",
							boxShadow: "0 4px 20px 0 rgba(88,101,242,0.3)",
						}}
					/>
					<Typography variant="h4" color="primary" sx={{fontWeight: 700, mb: 1}}>
						KVGG
					</Typography>
					<Typography
						variant="h6"
						color="white"
						align="center"
						sx={{fontWeight: 500, mb: 3, letterSpacing: 1}}
					>
						Login mit Discord
					</Typography>
					<Typography
						variant="body1"
						color="grey.300"
						align="center"
						sx={{mb: 3, lineHeight: 1.6}}
					>
						Melde dich mit deinem Discord-Account an, um Zugriff auf unsere Plattform zu erhalten.
					</Typography>
					<Button
						onClick={handleLogin}
						variant="contained"
						color="primary"
						fullWidth
						sx={{
							py: 1.5,
							fontWeight: 600,
							fontSize: "1.1rem",
							borderRadius: 2,
							boxShadow: "0 2px 8px 0 rgba(88,101,242,0.15)",
							mb: 2,
							textTransform: "none",
						}}
						startIcon={
							<img
								src="Discord/Clyde.svg"
								style={{width: 28, height: 28, background: "transparent"}}
								alt="Clyde"
							/>
						}
					>
						Login mit Discord
					</Button>
					<FormControlLabel
						control={
							<Checkbox
								checked={remindMe}
								onChange={() => setRemindMe(!remindMe)}
								color="primary"
								sx={{color: "#94a3b8"}}
							/>
						}
						label={
							<Typography variant="body2" color="grey.300">
								Erinnern für 14 Tage?
							</Typography>
						}
						sx={{mb: 1}}
					/>
				</Paper>
			</Box>
			<Copyright/>
		</Box>
	);
}

export default Login;