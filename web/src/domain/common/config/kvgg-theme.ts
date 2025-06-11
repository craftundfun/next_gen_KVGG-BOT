import {createTheme} from "@mui/material";

const kvggTheme = createTheme({
	palette: {
		mode: "dark",
		primary: {
			main: '#2196f3',
		},
		secondary: {
			main: '#ff9800',
		},
	},
	typography: {
		fontFamily: 'Titillium Web',
	},
});

export default kvggTheme;