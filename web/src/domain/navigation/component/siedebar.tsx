import React from 'react';
import {
	Box,
	Drawer,
	List,
	ListItem,
	ListItemIcon,
	ListItemText,
	Typography,
	Divider,
	LinearProgress,
	Select,
	MenuItem,
	FormControl,
	InputLabel,
} from '@mui/material';
import DashboardIcon from '@mui/icons-material/Dashboard';

const drawerWidth = 260;

const Sidebar: React.FC = () => {
	return (
		<Drawer
			variant="permanent"
			sx={{
				width: drawerWidth,
				flexShrink: 0,
				'& .MuiDrawer-paper': {
					width: drawerWidth,
					boxSizing: 'border-box',
					backgroundColor: '#0f172a',
					color: '#fff',
					borderRight: 'none',
				},
			}}
		>
			<Box sx={{ padding: 2 }}>
				<Typography variant="h6" sx={{ mb: 2 }}>
					Discord Dashboard
				</Typography>

				<FormControl fullWidth variant="outlined" size="small" sx={{ mb: 2 }}>
					<InputLabel sx={{ color: '#fff' }}>Discord-User auswählen</InputLabel>
					<Select defaultValue="Alex" label="Discord-User auswählen" sx={{ color: '#fff' }}>
						<MenuItem value="Alex">Alex</MenuItem>
					</Select>
				</FormControl>

				<List>
					<ListItem>
						<ListItemIcon>
							<DashboardIcon />
						</ListItemIcon>
						<ListItemText primary="Overview" secondary="Deine Statistiken pro Server"/>
					</ListItem>
					<ListItem>
						<ListItemIcon>
							<DashboardIcon />
						</ListItemIcon>
						<ListItemText primary="Online-Statistik" />
					</ListItem>
					<ListItem>
						<ListItemIcon>
							<DashboardIcon />
						</ListItemIcon>
						<ListItemText primary="Historische Aktivität" />
					</ListItem>
					<ListItem>
						<ListItemIcon>
							<DashboardIcon />
						</ListItemIcon>
						<ListItemText primary="Top Beziehungen" />
					</ListItem>
					<ListItem>
						<ListItemIcon>
							<DashboardIcon />
						</ListItemIcon>
						<ListItemText primary="Aktivitätenkalender" />
					</ListItem>
					<ListItem>
						<ListItemIcon>
							<DashboardIcon/>
						</ListItemIcon>
						<ListItemText primary="Badges" />
					</ListItem>
				</List>

				<Divider sx={{ backgroundColor: '#334155', my: 2 }} />

				<Box>
					<Typography variant="body2" sx={{ mb: 1 }}>
						Fortschritt Online-Ziel:
					</Typography>
					<LinearProgress variant="determinate" value={75} sx={{ height: 8, borderRadius: 5, backgroundColor: '#1e293b', '& .MuiLinearProgress-bar': { backgroundColor: '#6366f1' } }} />
					<Typography variant="caption" sx={{ mt: 1, display: 'block' }}>
						75 / 100 Stunden
					</Typography>
				</Box>
			</Box>
		</Drawer>
	);
};

export default Sidebar;
