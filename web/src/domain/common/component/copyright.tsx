import {Button} from "@/domain/ui/component/button.tsx";
import * as React from "react";

function Copyright(): React.ReactNode {
	return (
		<p className="text-center text-muted-foreground">
			{'Copyright ©'}
			<Button variant="link" onClick={() => window.open('https://kvgg.axellotl.de', '_blank')}>
				KVGG
			</Button>
			{new Date().getFullYear()}
		</p>
	);
}

export default Copyright;