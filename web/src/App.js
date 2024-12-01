import React, {useEffect, useState} from 'react';

function App() {
	const [message, setMessage] = useState("");

	useEffect(() => {
		fetch('http://localhost:8000/api/hello')
			.then(response => response.json())
			.then(data => setMessage(data.message + " And hello from Rene! :)"));
	}, []);

	// return (
	// 	<div className="App">
	// 		<h1>{message}</h1>
	// 	</div>
	// );

	return (
		<div className="App">
			<h1>Show and tell</h1>
			<button
				onClick={(e) =>
					window.open(
						"https://discord.com/oauth2/authorize?client_id=1076510738576855051&response_type=code&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Fauth%2Fdiscord&scope=identify",
						"_parent"
					)
				}
			>
				Auth
			</button>
		</div>
	);
}

export default App;
