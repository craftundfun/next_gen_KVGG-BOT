import React from 'react';
import {BrowserRouter as Router, Route, Routes,} from "react-router-dom";
import Error from '@components/Status/Error';
import Forbidden from '@components/Status/Forbidden';
import Dashboard from '@components/Dashboard/Dashboard';
import LoginScreen from '@components/Login/LoginScreen';
import {WebsiteUserProvider} from '@context/WebsiteUserContext';
import {DiscordUserProvider} from '@context/DiscordUserContext';
import {GuildProvider} from '@context/GuildContext';
import {GuildDiscordUserMappingProvider} from '@context/GuildDiscordUserMappingContext';
import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';
import {theme} from '@modules/Theme';
import {ThemeProvider} from '@mui/material/styles';
import {CssBaseline} from '@mui/material';


function App() {
	return (
		<ThemeProvider theme={theme}>
			<CssBaseline/>
			<Router>
				<WebsiteUserProvider>
					<DiscordUserProvider>
						<GuildProvider>
							<GuildDiscordUserMappingProvider>
								<Routes>
									(// login page)
									<Route
										path="/"
										element={
											<LoginScreen/>
										}
									/>
									<Route
										path="/dashboard"
										element={
											<Dashboard/>
										}>
									</Route>
									<Route
										path="*"
										element={
											<div>Page Not Found</div>
										}
									/>
									<Route
										path="/forbidden"
										element={
											<Forbidden/>
										}
									/>
									<Route
										path="/error"
										element={
											<Error/>
										}
									/>
								</Routes>
							</GuildDiscordUserMappingProvider>
						</GuildProvider>
					</DiscordUserProvider>
				</WebsiteUserProvider>
			</Router>
		</ThemeProvider>
	);
}

export default App;


