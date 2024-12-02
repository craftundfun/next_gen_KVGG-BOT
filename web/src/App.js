import React from 'react';
import {BrowserRouter as Router, Route, Routes,} from "react-router-dom";
import Login from './assets/Components/Login/Login.tsx';
import Dashboard from './assets/Components/Dashboard/Dashboard.tsx';
import Forbidden from './assets/Components/Status/Forbidden.tsx';
import LoginRedirect from './assets/Components/Login/LoginRedirect.tsx';
import Error from './assets/Components/Status/Error.tsx';

function App() {
	return (
		<Router>
			<Routes>
				<Route path="/" element={<Login/>}/>
				<Route path="/login" element={<LoginRedirect/>}/>
				<Route path="/dashboard" element={<Dashboard/>}/>

				<Route path="*" element={<div>Page Not Found</div>}/>
				<Route path="/forbidden" element={<Forbidden/>}/>
				<Route path="/error" element={<Error/>}/>
			</Routes>
		</Router>
	);
}

export default App;


