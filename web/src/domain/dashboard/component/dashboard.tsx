import * as React from "react";
import {Suspense} from "react";
import sleep from "../../common/helper/sleep.ts";

function Dashboard(): React.ReactNode {
	const loadComponents = async (): Promise<string> => {
		await sleep(3_000);
		return 'Dashboard';
	}

	return (
		<Suspense fallback={"Loading ...."}>
			{ loadComponents() }
		</Suspense>
	);
}

export default Dashboard;