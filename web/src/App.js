import React from 'react';
import {BrowserRouter as Router, Route, Routes,} from "react-router-dom";
import Login from '@/components/ui/Login/Login.tsx';
import Dashboard from '@/components/ui/Dashboard/Dashboard.tsx';
import Forbidden from '@/components/ui/Status/Forbidden.tsx';
import LoginRedirect from '@/components/ui/Login/LoginRedirect.tsx';
import Error from '@/components/ui/Status/Error.tsx';
import {AuthProvider} from './modules/AuthContext.tsx';
import ProtectedRoute from './modules/ProtectedRoute.tsx';

function App() {
	return (
		<AuthProvider>
			<Router>
				<Routes>
					(// login page)
					<Route path="/" element={<Login/>}/>
					<Route path="/login" element={<LoginRedirect/>}/>

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


