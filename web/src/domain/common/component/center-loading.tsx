import * as React from "react";

function CenterLoading(): React.ReactNode {
	return (
		<div className="fixed inset-0 flex flex-col items-center justify-center bg-background z-50">
			<div className="w-12 h-12 border-4 border-primary border-t-transparent rounded-full animate-spin mb-4" />
			<span className="text-2xl font-bold text-primary animate-pulse animate-bounce-slow"></span>
		</div>
	);
}

export default CenterLoading;