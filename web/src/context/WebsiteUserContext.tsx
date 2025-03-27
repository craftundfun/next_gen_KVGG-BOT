import React, {createContext, useContext, useState, ReactNode, useEffect} from 'react';
import {WebsiteUser} from "@customTypes/WebsiteUser";
import {useLocation} from "react-router-dom";

interface WebsiteUserContextType {
	websiteUser: WebsiteUser | null;
	setWebsiteUser: (user: WebsiteUser) => void;
}

const WebsiteUserContext = createContext<WebsiteUserContextType | undefined>(undefined);

interface Props {
	children: ReactNode;
}

export const WebsiteUserProvider: React.FC<Props> = ({children}) => {
	const location = useLocation();

	const [websiteUser, setWebsiteUserState] = useState<WebsiteUser | null>(() => {
		const storedUser = sessionStorage.getItem('websiteUser');

		if (storedUser === null) {
			return null;
		}

		const user: WebsiteUser = JSON.parse(storedUser);

		if (user.discord_id === null || user.discord_id === undefined) {
			return null;
		}

		return user;
	});

	const setWebsiteUser = (user: WebsiteUser) => {
		sessionStorage.setItem('websiteUser', JSON.stringify(user));

		setWebsiteUserState(user);
	};

	// Fetch the website user when the component mounts or when the location changes
	useEffect(() => {
		if (location.pathname === "/dashboard") {
			fetch("/api/websiteUser/me", {
				method: "GET",
				headers: {
					"Content-Type": "application/json",
				},
				credentials: "include",
			})
				.then((response) => response.json())
				.then((data) => {
					if (data) {
						setWebsiteUser(data);
					}
				})
				.catch((error) => {
					console.error("Error fetching website user:", error);
				});
		}
	}, [location.pathname]);

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