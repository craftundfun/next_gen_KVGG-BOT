import * as React from "react";
import {Suspense} from "react";
import sleep from "../../common/util/sleep.ts";
import DashboardSkeleton from "./dashboard-skeleton.tsx";

function Dashboard(): React.ReactNode {
	const loadComponents = async (): Promise<string> => {
		await sleep(3_000);
		return 'Dashboard';
	}

	return (
			<Suspense fallback={<DashboardSkeleton/>}>
				{loadComponents()}
			</Suspense>
	);
}

export default Dashboard;