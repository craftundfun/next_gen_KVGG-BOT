import * as React from "react";
import {Button} from "@ui/button";
import {Card, CardContent, CardHeader, CardTitle} from "@ui/card";
import {Avatar, AvatarFallback, AvatarImage} from "@ui/avatar";
import {discordOAuthUrl} from "@modules/Constants";

function Login() {
	const handleLogin = () => {
		window.open(discordOAuthUrl, "_parent");
	};

	return (
		<div className="flex flex-col justify-between h-screen bg-gradient-to-b from-gray-900 to-gray-800">
			<div className="flex items-center justify-center h-full">
				<Card
					className="flex flex-col items-center justify-center w-1/3 max-w-full max-h-full p-6 shadow-xl overflow-hidden">
					<CardHeader className="flex flex-col items-center space-y-2">
						<Avatar className="w-16 h-16">
							<AvatarImage src="/KVGG/KVGG Logo Icon.png"/>
							<AvatarFallback>Discord</AvatarFallback>
						</Avatar>
						<p className="text-white text-xl">KVGG</p>
					</CardHeader>
					<CardTitle className="text-primary text-2xl text-center">
						Login mit Discord
					</CardTitle>
					<CardContent className="flex flex-col items-center mt-8 space-y-4">
						<p className="text-gray-400 text-center">
							Melde dich mit deinem Discord-Account an, um Zugriff auf unsere Plattform zu erhalten.
						</p>
						<Button
							onClick={handleLogin}
							className="bg-primary hover:bg-secondary text-white px-4 py-2 rounded-lg w-full"
						>
							Login mit Discord
						</Button>
					</CardContent>
				</Card>
			</div>
			<div>
				<p className="text-white text-center">
					© 2024 <a href="https://github.com/craftundfun" className="underline text-accent">craftundfun</a>.
					All
					rights reserved.
				</p>
			</div>
		</div>
	);
}

export default Login;