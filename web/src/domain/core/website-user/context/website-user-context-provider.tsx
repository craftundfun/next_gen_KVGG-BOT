import {useQuery} from "@tanstack/react-query";
import {useEffect} from "react";
import * as React from "react";
import {useNavigate} from "react-router-dom";
import fetchWebsiteUser from "../http/fetch-user.ts";
import {websiteUserContext} from "./website-user-context";


function WebsiteUserContextProvider({children}: React.PropsWithChildren): React.ReactNode {
	const navigate = useNavigate();
	const {data: websiteUser, isError, isFetching} = useQuery({
		queryKey: ['websiteUser'],
		queryFn: fetchWebsiteUser,
		retry: false,
	});

	useEffect(() => {
		if (websiteUser) {
			navigate('/dashboard');
		}

		if ((isError || !websiteUser) && !isFetching) {
			navigate('/login');
		}
	}, [isError, websiteUser, isFetching, navigate]);

	if (isFetching) {
		return <>Loading</>;
	}

	return <websiteUserContext.Provider value={{websiteUser: websiteUser ?? null}}>
		{children}
	</websiteUserContext.Provider>
}

export default WebsiteUserContextProvider;