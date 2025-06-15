import * as React from 'react';
import {Box, CircularProgress} from "@mui/material";

function CenterLoading(): React.ReactNode {
	return (
		<Box
			display="flex"
			justifyContent="center"
			alignItems="center"
			height="100%"
		>
			<CircularProgress/>
		</Box>
	)
}

export default CenterLoading;