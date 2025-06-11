import {ThemeProvider} from "@mui/material";
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
					<WebsiteUserContextProvider>
						<Routes/>
					</WebsiteUserContextProvider>
				</ThemeProvider>
			</QueryClientProvider>
		</BrowserRouter>
	);
}

export default App
