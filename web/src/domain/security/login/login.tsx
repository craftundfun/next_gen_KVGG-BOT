import * as React from "react";
import { useState } from "react";
import { Button } from "@/domain/ui/component/button";
import { Checkbox } from "@/domain/ui/component/checkbox";
import { Card, CardContent } from "@/domain/ui/component/card";
import { Avatar } from "@/domain/ui/component/avatar";
import { Label } from "@/domain/ui/component/label";
import Copyright from "../../common/component/copyright.tsx";

function Login(): React.ReactNode {
	const [remindMe, setRemindMe] = useState<boolean>(false);

	const handleLogin = () => {
		const redirectUri = import.meta.env.VITE_DISCORD_OAUTH_URL;
		window.open(
			redirectUri + "&state=remindMe=" + remindMe.toString().toLowerCase(),
			"_parent"
		);
	};

	return (
		<div className="min-h-screen min-w-screen bg-gradient-to-br from-[rgba(30,41,59,0.85)] to-primary/30 flex flex-col justify-between">
			<div className="flex flex-1 items-center justify-center">
				<Card className="min-w-[350px] max-w-[400px] p-8 rounded-2xl border border-white/10 shadow-[0_8px_32px_0_rgba(31,38,135,0.37)] bg-[rgba(30,41,59,0.95)] backdrop-blur-[6px] flex flex-col items-center">
					<CardContent className="flex flex-col items-center gap-5 py-8 h-full justify-center">
						<Avatar className="w-20 h-20 mb-2 bg-primary shadow-lg">
							<img
								src="/KVGG/KVGG Logo Icon.png"
								alt="Discord"
								className="w-full h-full object-cover"
							/>
						</Avatar>
						<h4 className="font-bold text-primary">KVGG</h4>
						<p className="text-muted-foreground text-center">
							Melde dich mit deinem Discord-Account an, um Zugriff auf unsere Plattform zu erhalten.
						</p>
						<Button
							onClick={handleLogin}
							className="w-full flex text-base text-foreground light:text-secondary-foreground"
							variant="default"
						>
							<img
								src="Discord/Clyde.svg"
								alt="Clyde"
								className="w-6 h-6"
							/>
							Login mit Discord
						</Button>
						<div className="flex items-center w-full justify-center">
							<Checkbox
								id="remindMe"
								checked={remindMe}
								onCheckedChange={() => setRemindMe(!remindMe)}
							/>
							<Label htmlFor="remindMe" className="ml-2 text-muted-foreground">
								Erinnern für 14 Tage?
							</Label>
						</div>
					</CardContent>
				</Card>
			</div>
			<Copyright />
		</div>
	);
}

export default Login;