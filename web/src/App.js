import React from 'react';
import {BrowserRouter as Router, Route, Routes,} from "react-router-dom";
import Error from '@components/Status/Error';
import {AuthProvider} from '@context/AuthContext';
import ProtectedRoute from '@modules/ProtectedRoute';
import Forbidden from '@components/Status/Forbidden';
import Dashboard from '@components/Dashboard/Dashboard';
import Login from '@components/Login/Login';
import LoginScreen from '@components/Login/LoginScreen';

function App() {
	return (
		<AuthProvider>
			<Router>
				<Routes>
					(// login page)
					<Route path="/" element={<LoginScreen/>}/>
					<Route path="/login" element={<Login/>}/>

					<Route
						path="/dashboard"
						element={
							<ProtectedRoute>
								<Dashboard/>
							</ProtectedRoute>
						}>
					</Route>


					<Route path="*" element={<div>Page Not Found</div>}/>
					<Route path="/forbidden" element={<Forbidden/>}/>
					<Route path="/error" element={<Error/>}/>
				</Routes>
			</Router>
		</AuthProvider>
	);
}

export default App;


