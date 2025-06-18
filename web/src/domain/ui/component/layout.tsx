import useWebsiteUserContext from "@/domain/core/website-user/hook/use-website-user-context.ts";
import KvggSidebar from "@/domain/navigation/component/kvgg-sidebar.tsx";
import * as React from "react"
import { SidebarProvider } from "@/domain/ui/component/sidebar"

function Layout({ children }: { children: React.ReactNode }) {
	const { websiteUser } = useWebsiteUserContext();

	if (!websiteUser) {
		return (<>{children}</>);
	}

	return (
		<SidebarProvider>
			<KvggSidebar />
			<main className="flex-1 p-4">
				{children}
			</main>
		</SidebarProvider>
	)
}

export default Layout;