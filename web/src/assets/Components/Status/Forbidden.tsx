import React from "react";
import BaseLayout from "@modules/SiteBlueprint";
import {Typography} from "@mui/material";

function Forbidden() {
	return (
		<BaseLayout>
			<div>
				<Typography variant="h4" color="error">Forbidden</Typography>
				<Typography variant="body1" color="white">
					You cant login here! You aren’t or weren’t on a server with the bot!
				</Typography>
			</div>
		</BaseLayout>
	);
}

export default Forbidden;