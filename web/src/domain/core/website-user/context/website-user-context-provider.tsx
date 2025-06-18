import {useQuery, useQueryClient} from "@tanstack/react-query";
import {useEffect} from "react";
import * as React from "react";
import {useNavigate} from "react-router-dom";
import CenterLoading from "../../../common/component/center-loading.tsx";
import fetchWebsiteUser from "../http/fetch-user.ts";
import {websiteUserContext} from "./website-user-context";


function WebsiteUserContextProvider({children}: React.PropsWithChildren): React.ReactNode {
	const navigate = useNavigate();
	const queryClient = useQueryClient()
	const {data: websiteUser, isError, isFetching} = useQuery({
		queryKey: ['websiteUser'],
		queryFn: fetchWebsiteUser,
		retry: false,
	});

	useEffect(() => {
		if (isError) {
			queryClient.setQueryData(['websiteUser'], () => null);
		}

		if ((isError || !websiteUser?.email) && !isFetching) {
			navigate('/login');
		}
	}, [isError, websiteUser?.email, isFetching, navigate, queryClient]);

	if (isFetching) {
		return <CenterLoading/>;
	}

	return <websiteUserContext.Provider value={{websiteUser: websiteUser ?? null}}>
		{children}
	</websiteUserContext.Provider>
}

export default WebsiteUserContextProvider;