import { Home, UserRound, Settings } from "lucide-react"
import {
	Sidebar,
	SidebarContent,
	SidebarGroup,
	SidebarGroupContent,
	SidebarGroupLabel,
	SidebarMenu,
	SidebarMenuButton,
	SidebarMenuItem,
} from "@/domain/ui/component/sidebar"
import {type NavigateFunction, useNavigate} from "react-router-dom";
import type { LucideIcon } from "lucide-react";

interface SidebarItem {
	title: string;
	url: string;
	icon: LucideIcon;
}

const items: SidebarItem[] = [
	{
		title: "Dashboard",
		url: "/dashboard",
		icon: Home,
	},
	{
		title: "Profile",
		url: "/profile",
		icon: UserRound,
	},
	{
		title: "Settings",
		url: "/404",
		icon: Settings,
	},
]

function KvggSidebar() {
	const navigate: NavigateFunction = useNavigate();

	return (
		<Sidebar collapsible="icon">
			<SidebarContent>
				<SidebarGroup>
					<SidebarGroupLabel>KVGG</SidebarGroupLabel>
					<SidebarGroupContent>
						<SidebarMenu>
							{items.map((item) => (
								<SidebarMenuItem key={item.title}>
									<SidebarMenuButton asChild>
										<a onClick={(): void | Promise<void> => navigate(item.url)}>
											<item.icon />
											<span>{item.title}</span>
										</a>
									</SidebarMenuButton>
								</SidebarMenuItem>
							))}
						</SidebarMenu>
					</SidebarGroupContent>
				</SidebarGroup>
			</SidebarContent>
		</Sidebar>
	)
}

export default KvggSidebar;