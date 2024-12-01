import React, {useEffect, useState} from 'react';

function App() {
	const [message, setMessage] = useState("");

	useEffect(() => {
		fetch('http://localhost:8000/api/hello')
			.then(response => response.json())
			.then(data => setMessage(data.message + " And hello from React!"));
	}, []);

	return (
		<div className="App">
			<h1>{message}</h1>
		</div>
	);
}

export default App;
