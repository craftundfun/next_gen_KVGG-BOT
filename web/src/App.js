import React from 'react';
import {BrowserRouter as Router, Route, Routes,} from "react-router-dom";
import Error from '@components/Status/Error';
import {AuthProvider} from '@context/AuthContext';
import Forbidden from '@components/Status/Forbidden';
import Dashboard from '@components/Dashboard/Dashboard';
import LoginScreen from '@components/Login/LoginScreen';
import {WebsiteUserProvider} from '@context/WebsiteUserContext';
import {DiscordUserProvider} from '@context/DiscordUserContext';
import {GuildProvider} from '@context/GuildContext';
import ProtectedRoute from '@modules/ProtectedRoute';

function App() {
	return (
		<Router>
			<AuthProvider>
				<WebsiteUserProvider>
					<DiscordUserProvider>
						<GuildProvider>
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
										<ProtectedRoute>
											<Dashboard/>
										</ProtectedRoute>
									}>
								</Route>
								<Route
									path="*"
									element={
										<ProtectedRoute>
											<div>Page Not Found</div>
										</ProtectedRoute>
									}
								/>
								<Route
									path="/forbidden"
									element={
										<ProtectedRoute>
											<Forbidden/>
										</ProtectedRoute>
									}
								/>
								<Route
									path="/error"
									element={
										<ProtectedRoute>
											<Error/>
										</ProtectedRoute>
									}
								/>
							</Routes>
						</GuildProvider>
					</DiscordUserProvider>
				</WebsiteUserProvider>
			</AuthProvider>
		</Router>

	);
}

export default App;


