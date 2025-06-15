import * as React from "react";
import {lazy, Suspense} from "react";
import {Navigate, Route, Routes,} from "react-router-dom";
import CenterLoading from "../../common/component/center-loading.tsx";
import Login from "../../security/login/login.tsx";


function Router(): React.ReactNode {
	const Dashboard = lazy(() => import("../../dashboard/component/dashboard.tsx"));

	return (
		<Suspense fallback={<CenterLoading/>}>
			<Routes>
				<Route path="/login" element={<Login/>}/>
				<Route path="/dashboard" element={<Dashboard/>}/>
				<Route path="/profile" element={<div>Profile</div>}/>
				<Route path="/404" element={<div>Not Found</div>}/>
				<Route path="*" element={<Navigate to="/404" replace/>}/>
			</Routes>
		</Suspense>
	);
}

export default Router;
