import {Button} from "@/domain/ui/component/button";
import {Drawer, DrawerContent, DrawerHeader, DrawerTitle,} from "@/domain/ui/component/drawer";
import {Progress} from "@/domain/ui/component/progress";
import {Select, SelectContent, SelectItem, SelectTrigger, SelectValue} from "@/domain/ui/component/select";
import {Separator} from "@/domain/ui/component/separator";
import {LayoutDashboard} from "lucide-react";
import * as React from "react";

const Sidebar: React.FC = () => {
	return (
		<Drawer open={true} direction="left">
			<DrawerContent>
				<DrawerHeader>
					<DrawerTitle className="mb-4">Discord Dashboard</DrawerTitle>
					<Select defaultValue="Alex">
						<SelectTrigger className="mb-4 text-white bg-slate-800 border-slate-700">
							<SelectValue placeholder="Discord-User auswählen"/>
						</SelectTrigger>
						<SelectContent>
							<SelectItem value="Alex">Alex</SelectItem>
						</SelectContent>
					</Select>
				</DrawerHeader>
				<nav className="px-4">
					<ul className="space-y-2">
						<li>
							<Button variant="ghost" className="w-full justify-start text-white">
								<LayoutDashboard className="mr-2"/>
								Overview
							</Button>
						</li>
						<li>
							<Button variant="ghost" className="w-full justify-start text-white">
								<LayoutDashboard className="mr-2"/>
								Online-Statistik
							</Button>
						</li>
						<li>
							<Button variant="ghost" className="w-full justify-start text-white">
								<LayoutDashboard className="mr-2"/>
								Historische Aktivität
							</Button>
						</li>
						<li>
							<Button variant="ghost" className="w-full justify-start text-white">
								<LayoutDashboard className="mr-2"/>
								Top Beziehungen
							</Button>
						</li>
						<li>
							<Button variant="ghost" className="w-full justify-start text-white">
								<LayoutDashboard className="mr-2"/>
								Aktivitätenkalender
							</Button>
						</li>
						<li>
							<Button variant="ghost" className="w-full justify-start text-white">
								<LayoutDashboard className="mr-2"/>
								Badges
							</Button>
						</li>
					</ul>
				</nav>
				<Separator className="my-6 bg-slate-700"/>
				<div className="px-4">
					<div className="mb-2 text-sm">Fortschritt Online-Ziel:</div>
					<Progress value={75} className="h-2 rounded bg-slate-800"/>
					<div className="mt-2 text-xs">75 / 100 Stunden</div>
				</div>
			</DrawerContent>
		</Drawer>
	);
};

export default Sidebar;