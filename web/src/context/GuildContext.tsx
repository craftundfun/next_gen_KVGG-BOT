import React, {createContext, useContext, useState, ReactNode} from 'react';
import {Guild} from "@customTypes/Guild";

interface GuildContextType {
	guild: Guild | null;
	setGuild: (user: Guild) => void;
}

const GuildContext = createContext<GuildContextType | undefined>(undefined);

interface Props {
	children: ReactNode;
}

export const GuildProvider: React.FC<Props> = ({children}) => {
	const [guild, setGuildState] = useState<Guild | null>(() => {
		const storedGuild = sessionStorage.getItem('guild');

		return storedGuild ? JSON.parse(storedGuild) : null;
	});

	const setGuild = (guild: Guild) => {
		sessionStorage.setItem('guild', JSON.stringify(guild));

		setGuildState(guild);
	};

	return (
		<GuildContext.Provider value={{guild: guild, setGuild: setGuild}}>
			{children}
		</GuildContext.Provider>
	);
};

export const useGuild = (): GuildContextType => {
	const context = useContext(GuildContext);

	if (!context) {
		throw new Error('useGuild must be used within a GuildProvider');
	}

	return context;
};