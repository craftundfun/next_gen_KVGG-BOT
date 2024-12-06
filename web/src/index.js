import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import {DiscordUserProvider} from './context/DiscordUserContext';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
	<React.StrictMode>
		<DiscordUserProvider>
			<App/>
		</DiscordUserProvider>
	</React.StrictMode>
);
