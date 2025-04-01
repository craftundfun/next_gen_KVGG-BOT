import React from 'react';
import BaseLayout from "@ui/SiteBlueprint";
import Statistics from "@components/Dashboard/PersonalInfo/Statistics";
import StatisticGraph from "@components/Dashboard/PersonalInfo/StatisticGraph";

function Dashboard() {
	return (
		<div>
			<BaseLayout>
				{(
					<div className=" flex-grow grid grid-cols-2 grid-rows-2 h-full">
						<div className="overflow-auto">
							<p>Test</p>
						</div>
						<div className="overflow-auto">
							<p>Test1</p>
						</div>
						<div className="overflow-auto">
							<StatisticGraph/>
						</div>
						<div className="overflow-auto">
							<Statistics/>
						</div>
					</div>
				)}
			</BaseLayout>
		</div>
	);
}

export default Dashboard;
