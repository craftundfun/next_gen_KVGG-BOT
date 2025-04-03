import * as React from "react";
import {AppBar, Toolbar, Typography, Box} from "@mui/material";
import {useDiscordUser} from "@context/DiscordUserContext";
import {useWebsiteUser} from "@context/WebsiteUserContext";
import AvatarNameCombination from "@modules/AvatarSiteBlueprint";
import {useGuild} from "@context/GuildContext";
import {useGuildDiscordUserMapping} from "@context/GuildDiscordUserMappingContext";
import Drawer from '@mui/material/Drawer';
import {useState} from "react";
import List from '@mui/material/List';
import Divider from '@mui/material/Divider';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import Button from "@mui/material/Button";
import MenuIcon from '@mui/icons-material/Menu';
import HomeIcon from '@mui/icons-material/Home';
import {useNavigate} from "react-router-dom";
import ClearIcon from '@mui/icons-material/Clear';
import ErrorIcon from '@mui/icons-material/Error';


interface BaseLayoutProps {
	children: React.ReactNode;
}

const BaseLayout: React.FC<BaseLayoutProps> = ({children}) => {
	const {discordUser} = useDiscordUser();
	const {websiteUser} = useWebsiteUser();
	const {guild} = useGuild();
	const {guildDiscordUserMapping} = useGuildDiscordUserMapping();
	const navigate = useNavigate();

	const [open, setOpen] = useState(false);

	const toggleDrawer = (open: boolean) => () => {
		setOpen(open);
	};

	const DrawerList = (
		<Box sx={{width: 250, backgroundColor: "#1f1f1f"}} role="presentation" onClick={toggleDrawer(false)}>
			<List>
				<ListItem key={"Dashboard"} disablePadding>
					<ListItemButton onClick={() => navigate("/dashboard")}>
						<ListItemIcon>
							<HomeIcon color="primary"/>
						</ListItemIcon>
						<ListItemText primary={"Dashboard"} sx={{color: "white"}}/>
					</ListItemButton>
				</ListItem>
			</List>
			<Divider color="white"/>
			<List>
				<ListItem key={"Forbidden"} disablePadding>
					<ListItemButton onClick={() => navigate("/forbidden")}>
						<ListItemIcon>
							<ClearIcon color="warning"/>
						</ListItemIcon>
						<ListItemText primary={"Forbidden"} sx={{color: "white"}}/>
					</ListItemButton>
				</ListItem>
				<ListItem key={"Error"} disablePadding>
					<ListItemButton onClick={() => navigate("/error")}>
						<ListItemIcon>
							<ErrorIcon color="error"/>
						</ListItemIcon>
						<ListItemText primary={"Error"} sx={{color: "white"}}/>
					</ListItemButton>
				</ListItem>
			</List>
		</Box>
	);

	return (
		<div className="flex flex-col h-screen bg-gradient-to-b from-gray-900 to-gray-800">
			<Box sx={{height: "100vh", overflow: "auto"}}>
				<AppBar
					position="sticky"
					sx={{
						backgroundColor: "#1f1f1f",
						zIndex: 1000,
					}}
				>
					<Toolbar sx={{
						display: "flex",
						justifyContent: "space-between",
						alignItems: "center",
						position: "relative"
					}}>
						<Button onClick={toggleDrawer(true)} sx={{marginLeft: -4}}>
							<MenuIcon/>
						</Button>
						<Drawer open={open} onClose={toggleDrawer(false)} sx={{
							"& .MuiDrawer-paper": {
								backgroundColor: "#1f1f1f", // Hintergrundfarbe des Drawers
								color: "white", // Standard-Textfarbe innerhalb des Drawers
								width: 250, // Breite des Drawers
							}
						}}>
							{DrawerList}
						</Drawer>

						<Typography variant="h5" sx={{
							color: "white",
							position: "absolute",
							left: "50%",
							transform: "translateX(-50%)"
						}}>
							KVGG
						</Typography>

						<AvatarNameCombination
							discordUser={discordUser}
							websiteUser={websiteUser}
							guildDiscordUserMapping={guildDiscordUserMapping}
						/>
					</Toolbar>
				</AppBar>

				<Box sx={{flexGrow: 1, overflow: "auto", padding: 2}}>
					{children}
				</Box>
			</Box>
		</div>
	);
};

export default BaseLayout;
