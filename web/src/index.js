import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import {DiscordUserProvider} from '@context/DiscordUserContext';
import {WebsiteUserProvider} from '@context/WebsiteUserContext';

// eslint-disable-next-line no-undef
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
	<React.StrictMode>
		<DiscordUserProvider>
			<WebsiteUserProvider>
				<App/>
			</WebsiteUserProvider>
		</DiscordUserProvider>
	</React.StrictMode>
);
