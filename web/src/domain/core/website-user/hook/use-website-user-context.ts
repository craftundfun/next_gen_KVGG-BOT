import {useContext} from "react";
import {type WebsiteUserContext, websiteUserContext} from "../context/website-user-context.ts";

function useWebsiteUserContext(): WebsiteUserContext {
	const context = useContext<WebsiteUserContext | undefined>(websiteUserContext);

	if (!context) {
		throw new Error("useWebsiteUser must be used within a WebsiteUserProvider");
	}

	return context;
}

export default useWebsiteUserContext;