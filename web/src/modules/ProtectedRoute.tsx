import React, {ReactNode, useEffect} from "react";
import {useAuth} from "./AuthContext";
import {useNavigate} from "react-router-dom";

type Props = {
	children: ReactNode;
};

const ProtectedRoute = ({children}: Props) => {
	const {jwt, isAuthenticated} = useAuth();

	console.log("JWT in context: ", jwt);
	console.log("Is Authenticated: ", isAuthenticated);


	const navigate = useNavigate();

	useEffect(() => {
		console.log("Checking authentication...");
		if (!isAuthenticated) {
			console.log("Not authenticated, redirecting...");
			navigate("/");
		}
	}, [isAuthenticated, navigate]);

	// If the user is authenticated, render the protected children
	if (!isAuthenticated) {
		return null;
	}

	return <>{children}</>;
};

export default ProtectedRoute;
