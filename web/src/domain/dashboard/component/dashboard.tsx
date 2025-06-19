import useDiscordGuildUserContext from "@/domain/core/discord-guild-user/hook/use-discord-guild-user-context.ts";
import * as React from "react";
import {Suspense} from "react";
import sleep from "../../common/util/sleep.ts";
import DashboardSkeleton from "./dashboard-skeleton.tsx";

function Dashboard(): React.ReactNode {
	const loadComponents = async (): Promise<string> => {
		await sleep(3_000);
		return 'Dashboard';
	}
	const {discordGuildUser} = useDiscordGuildUserContext();

	return (
			<Suspense fallback={<DashboardSkeleton/>}>
				{loadComponents()}
				{null !== discordGuildUser && <div>{discordGuildUser.global_name}</div>}
			</Suspense>
	);
}

export default Dashboard;