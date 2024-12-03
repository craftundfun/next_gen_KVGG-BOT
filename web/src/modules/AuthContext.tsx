import React, {createContext, ReactNode, useContext, useState} from 'react';
import {jwtDecode} from "jwt-decode";

type AuthContextType = {
	jwt: string | null;
	login: (token: string) => void;
	logout: () => void;
	isAuthenticated: boolean;
};

const AuthContext = createContext<AuthContextType>({
	jwt: null,
	login: () => {
	},
	logout: () => {
	},
	isAuthenticated: false,
});

type Props = {
	children: ReactNode;
};

export const AuthProvider = ({children}: Props) => {
	/*
	AuthProvider is a wrapper component that provides the AuthContext to all children components. It also provides
	functionality to login, logout and check if the user is authenticated.
	 */
	const [jwt, setJwt] = useState<string | null>(() => sessionStorage.getItem('jwt'));

	// Handle login functionality
	const login = (token: string | null) => {
		if (token === null) {
			return;
		}

		setJwt(token);
		sessionStorage.setItem('jwt', token);
	};

	// Handle logout functionality
	const logout = () => {
		setJwt(null);
		sessionStorage.removeItem('jwt');
	};

	// Handle token expiration
	const isTokenExpired = (token: string | null): boolean => {
		if (token === null) {
			return true;
		}

		try {
			const decoded: any = jwtDecode(token);
			// current time in seconds
			const currentTime = Date.now() / 1000;

			return decoded.exp < currentTime;
		} catch (error) {
			return true;
		}
	};

	// Always ensure isAuthenticated is a boolean value
	const isAuthenticated = !!jwt && !isTokenExpired(jwt);

	return (
		<AuthContext.Provider value={{jwt, login, logout, isAuthenticated}}>
			{children}
		</AuthContext.Provider>
	);
};


export const useAuth = () => {
	/*
	useAuth is a custom hook that returns the AuthContext.
	It is used to access the login, logout and isAuthenticated.
	It also throws an error if the hook is used outside the AuthProvider.
	 */
	const context = useContext(AuthContext);

	if (!context) {
		throw new Error('useAuth must be used within an AuthProvider');
	}

	return context;
};
