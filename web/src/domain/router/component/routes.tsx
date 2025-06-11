import * as React from "react";
import {Navigate, Route, Routes,} from "react-router-dom";
import Login from "../../security/login/login.tsx";


function Router(): React.ReactNode {
	return (
		<Routes>
			<Route path="/login" element={<Login/>}/>
			<Route path="/dashboard" element={<div>Dashboard</div>}/>
			<Route path="/profile" element={<div>Profile</div>}/>
			<Route path="/404" element={<div>Not Found</div>}/>
			 <Route path="*" element={<Navigate to="/404" replace/>}/>
		</Routes>
	)
}

export default Router;
