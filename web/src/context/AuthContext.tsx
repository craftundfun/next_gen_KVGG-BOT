import React, {createContext, ReactNode, useContext, useEffect, useState} from 'react';
import {useLocation} from "react-router-dom";

type AuthContextType = {
	login: () => void;
	logout: () => void;
	isAuthenticated: boolean;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

type Props = {
	children: ReactNode;
};

export const AuthProvider = ({children}: Props) => {
	const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
	const location = useLocation();

	const login = () => {
		setIsAuthenticated(true);
	};

	const logout = () => {
		setIsAuthenticated(false);
	};

	useEffect(() => {
		fetch("auth/loggedIn", {
			method: "GET",
			headers: {
				"Content-Type": "application/json",
			},
			credentials: "include",
		})
			.then((response) => {
				if (response.status !== 200) {
					logout();
				}

				login();
			})
			.catch((error) => {
				console.error("Error checking authentication:", error);
			});
	}, [location]);

	return (
		<AuthContext.Provider value={{login, logout, isAuthenticated}}>
			{children}
		</AuthContext.Provider>
	);
};

export const useAuth = () => {
	const context = useContext(AuthContext);

	if (!context) {
		throw new Error('useAuth must be used within an AuthProvider');
	}

	return context;
};
