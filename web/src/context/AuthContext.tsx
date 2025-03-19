import React, {createContext, ReactNode, useContext, useState} from 'react';
import Forbidden from "@components/Status/Forbidden";

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

	const login = () => {
		setIsAuthenticated(true);
	};

	const logout = () => {
		setIsAuthenticated(false);
	};

	// if (!isAuthenticated) {
	// 	return <Forbidden/>;
	// }

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
