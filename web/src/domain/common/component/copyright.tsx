import * as React from "react";
import {Typography} from "@mui/material";
import Link from '@mui/material/Link';


function Copyright(props: any): React.ReactNode {
	return (
		<Typography variant="body2" color="secondary" align="center" {...props}>
			{'Copyright © '}
			<Link color="inherit" href="https://kvgg.axellotl.de/">
				KVGG
			</Link>{' '}
			{new Date().getFullYear()}
			{'.'}
		</Typography>
	);
}

export default Copyright;