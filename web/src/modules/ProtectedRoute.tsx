import React, {ReactNode, useEffect} from "react";
import {useAuth} from "./AuthContext";
import {useNavigate} from "react-router-dom";

type Props = {
	children: ReactNode;
};

const ProtectedRoute = ({children}: Props) => {
	/*
	ProtectedRoute is a wrapper component that checks if the user is authenticated. If the user is not authenticated,
	they are redirected to the login page. If the user is authenticated, the children are rendered.
	 */
	const {isAuthenticated} = useAuth();
	const navigate = useNavigate();

	useEffect(() => {
		if (!isAuthenticated) {
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
