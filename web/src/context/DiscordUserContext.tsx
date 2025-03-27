import React, {createContext, useContext, useState, ReactNode, useEffect} from 'react';
import {DiscordUser} from "@customTypes/DiscordUser";
import {useWebsiteUser} from "@context/WebsiteUserContext";

interface DiscordUserContextType {
	discordUser: DiscordUser | null;
	setDiscordUser: (user: DiscordUser) => void;
}

const DiscordUserContext = createContext<DiscordUserContextType | undefined>(undefined);

interface Props {
	children: ReactNode;
}

export const DiscordUserProvider: React.FC<Props> = ({children}) => {
	const {websiteUser} = useWebsiteUser();

	const [discordUser, setDiscordUserState] = useState<DiscordUser | null>(() => {
		const storedUser = sessionStorage.getItem('discordUser');

		if (storedUser === null) {
			return null;
		}

		const user: DiscordUser = JSON.parse(storedUser);

		if (user.discord_id === null || user.discord_id === undefined) {
			return null;
		}

		return user;
	});

	const setDiscordUser = (user: DiscordUser) => {
		sessionStorage.setItem('discordUser', JSON.stringify(user));

		setDiscordUserState(user);
	};

	useEffect(() => {
		fetch("/api/discordUser/me", {
			method: "GET",
			headers: {
				"Content-Type": "application/json",
			},
			credentials: "include",
		})
			.then((response) => response.json())
			.then((data) => {
				if (data) {
					setDiscordUser(data);
				}
			})
			.catch((error) => {
				console.error("Error fetching Discord user:", error);
			});
	}, [websiteUser]);


	return (
		<DiscordUserContext.Provider value={{discordUser, setDiscordUser}}>
			{children}
		</DiscordUserContext.Provider>
	);
};

export const useDiscordUser = (): DiscordUserContextType => {
	const context = useContext(DiscordUserContext);

	if (!context) {
		throw new Error('useDiscordUser must be used within a DiscordUserProvider');
	}

	return context;
};