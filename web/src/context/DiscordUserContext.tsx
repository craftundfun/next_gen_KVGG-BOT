import React, {createContext, useContext, useState, ReactNode} from 'react';
import {DiscordUser} from "../types/DiscordUser";

interface DiscordUserContextType {
	discordUser: DiscordUser | null;
	setDiscordUser: (user: DiscordUser) => void;
}

const DiscordUserContext = createContext<DiscordUserContextType | undefined>(undefined);

interface Props {
	children: ReactNode;
}

export const DiscordUserProvider: React.FC<Props> = ({children}) => {
	const [discordUser, setDiscordUserState] = useState<DiscordUser | null>(() => {
		const storedUser = sessionStorage.getItem('discordUser');

		return storedUser ? JSON.parse(storedUser) : null;
	});

	const setDiscordUser = (user: DiscordUser) => {

		sessionStorage.setItem('discordUser', JSON.stringify(user));
		setDiscordUserState(user);
	};

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