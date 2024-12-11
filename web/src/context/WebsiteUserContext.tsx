import React, {createContext, useContext, useState, ReactNode} from 'react';
import {WebsiteUser} from "@customTypes/WebsiteUser";

interface WebsiteUserContextType {
	websiteUser: WebsiteUser | null;
	setWebsiteUser: (user: WebsiteUser) => void;
}

const WebsiteUserContext = createContext<WebsiteUserContextType | undefined>(undefined);

interface Props {
	children: ReactNode;
}

export const WebsiteUserProvider: React.FC<Props> = ({children}) => {
	const [websiteUser, setWebsiteUserState] = useState<WebsiteUser | null>(() => {
		const storedUser = sessionStorage.getItem('websiteUser');

		return storedUser ? JSON.parse(storedUser) : null;
	});

	const setWebsiteUser = (user: WebsiteUser) => {
		sessionStorage.setItem('websiteUser', JSON.stringify(user));

		setWebsiteUserState(user);
	};

	return (
		<WebsiteUserContext.Provider value={{websiteUser, setWebsiteUser}}>
			{children}
		</WebsiteUserContext.Provider>
	);
};

export const useWebsiteUser = (): WebsiteUserContextType => {
	const context = useContext(WebsiteUserContext);

	if (!context) {
		throw new Error('useWebsiteUser must be used within a WebsiteUserProvider');
	}

	return context;
};