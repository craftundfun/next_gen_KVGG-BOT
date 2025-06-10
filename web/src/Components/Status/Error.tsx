import React from "react";
import BaseLayout from "@modules/SiteBlueprint";
import {Typography} from "@mui/material";

function Error() {
	return (
		<BaseLayout>
			<div>
				<Typography variant="h4" color="warning">Something went wrong!</Typography>
			</div>
		</BaseLayout>
	);
}

export default Error;