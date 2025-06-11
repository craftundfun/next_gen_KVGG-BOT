import {createContext} from "react";
import type WebsiteUser from "../@types/website-user.ts";

export interface WebsiteUserContext {
	websiteUser: WebsiteUser | null;
}

export const websiteUserContext = createContext<WebsiteUserContext | undefined>(undefined);
