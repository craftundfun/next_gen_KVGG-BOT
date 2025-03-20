import React, {ReactNode, useEffect} from "react";
import {useNavigate} from "react-router-dom";
import {useAuth} from "@context/AuthContext";

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

	return <>{children}</>;
};

export default ProtectedRoute;
