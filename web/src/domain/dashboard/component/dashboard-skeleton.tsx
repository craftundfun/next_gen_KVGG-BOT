import {Skeleton} from "@/domain/ui/component/skeleton.tsx";
import * as React from "react";


function DashboardSkeleton(): React.ReactNode {
	return (
		<Skeleton className="w-32 h-6" />
	);
}

export default DashboardSkeleton;