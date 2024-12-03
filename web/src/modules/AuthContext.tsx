import React, {createContext, ReactNode, useContext, useState} from 'react';

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

	// Always ensure isAuthenticated is a boolean value
	const isAuthenticated = !!jwt;

	return (
		<AuthContext.Provider value={{jwt, login, logout, isAuthenticated}}>
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
