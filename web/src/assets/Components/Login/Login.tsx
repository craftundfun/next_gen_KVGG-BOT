import * as React from "react";
import {Button} from "../../UI/button";


function Login() {
	return (
		<div className="App">
			<h1>Login</h1>
			<Button onClick={() =>
				window.open(
					"https://discord.com/oauth2/authorize?client_id=1076510738576855051&response_type=code&" +
					"redirect_uri=http%3A%2F%2F127.0.0.1%3A3000%2Flogin&scope=identify",
					"_parent",
				)
			}
			>
				Log in with Discord
			</Button>
		</div>
	);
}

export default Login;