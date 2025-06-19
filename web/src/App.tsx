import DiscordGuildUserContextProvider
	from "@/domain/core/discord-guild-user/context/discord-guild-user-context-provider.tsx";
import {ThemeProvider} from "@/domain/ui/component/theme-provider.tsx";
import {QueryClient, QueryClientProvider} from "@tanstack/react-query";
import {BrowserRouter} from "react-router";
import WebsiteUserContextProvider from "./domain/core/website-user/context/website-user-context-provider.tsx";
import KvggRoutes from "@/domain/router/component/kvggRoutes.tsx";
import Layout from "@/domain/ui/component/layout.tsx";

function App() {
	const queryClient = new QueryClient();

	return (
		<BrowserRouter>
			<QueryClientProvider client={queryClient}>
				<ThemeProvider defaultTheme="system">
					<WebsiteUserContextProvider>
						<DiscordGuildUserContextProvider>
							<Layout>
								<KvggRoutes/>
							</Layout>
						</DiscordGuildUserContextProvider>
					</WebsiteUserContextProvider>
				</ThemeProvider>
			</QueryClientProvider>
		</BrowserRouter>
	);
}

export default App
