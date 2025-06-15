import {CssBaseline, ThemeProvider} from "@mui/material";
import Box from "@mui/material/Box";
import {QueryClient, QueryClientProvider} from "@tanstack/react-query";
import {BrowserRouter} from "react-router-dom";
import kvggTheme from "./domain/common/config/kvgg-theme.ts";
import WebsiteUserContextProvider from "./domain/core/website-user/context/website-user-context-provider.tsx";
import Routes from "./domain/router/component/routes.tsx";

function App() {
	const queryClient = new QueryClient();

	return (
		<BrowserRouter>
			<QueryClientProvider client={queryClient}>
				<ThemeProvider theme={kvggTheme}>
					<CssBaseline>
						<Box style={{width: "100dvw", height: "100dvh"}}>
							<WebsiteUserContextProvider>
								<Routes/>
							</WebsiteUserContextProvider>
						</Box>
					</CssBaseline>
				</ThemeProvider>
			</QueryClientProvider>
		</BrowserRouter>
	);
}

export default App
