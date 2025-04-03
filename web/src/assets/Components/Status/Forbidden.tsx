import React from "react";
import BaseLayout from "@modules/SiteBlueprint";
import {Button, Typography} from "@mui/material";
import ClearIcon from '@mui/icons-material/Clear';


function Forbidden() {
	return (
		<BaseLayout>
			<div className={"flex flex-col items-center justify-center h-full"}>
				<div className={"flex items-center space-x-3"}>
					<ClearIcon sx={{height: 100, width: 100, marginTop: 10}} color="error"/>
					<Typography variant="h1" color="error" sx={{marginTop: 10}}>
						Forbidden
					</Typography>
				</div>
				<Typography variant="h4" color="white" sx={{marginTop: 1}}>
					You are not logged in!
				</Typography>
				<Button variant="contained" sx={{marginTop: 2, width: 200, height: 50}}
						onClick={() => window.location.href = "/"}>
					<Typography variant="h5" color="white">
						Go to Login
					</Typography>
				</Button>
			</div>
		</BaseLayout>
	);
}

export default Forbidden;