import * as React from "react";
import {Avatar, AvatarFallback, AvatarImage} from "../ui/avatar";
import {useDiscordUser} from "../../../context/DiscordUserContext";
import {useWebsiteUser} from "../../../context/WebsiteUserContext";
import {Spinner} from "../ui/spinner";

interface BaseLayoutProps {
	children: React.ReactNode;
}

const BaseLayout: React.FC<BaseLayoutProps> = ({children}) => {
	const {discordUser} = useDiscordUser();
	const {websiteUser} = useWebsiteUser();

	return (
		<div className="flex flex-col h-screen bg-gradient-to-b from-gray-900 to-gray-800">
			<div className="relative flex items-center justify-between p-2 bg-gray-800"
				 style={{height: '8%', minHeight: '50px', maxHeight: '50px'}}>
				<div className="flex items-center">
					<Avatar className="mt-1 w-8 h-8">
						<AvatarImage src="/KVGG/KVGG Logo Icon.png"/>
						<AvatarFallback>KVGG Logo</AvatarFallback>
					</Avatar>
				</div>
				<div className="absolute left-1/2 transform -translate-x-1/2 text-white text-3xl underline">
					KVGG
				</div>
				<div className="flex items-center">
					<div className="text-white">
						{discordUser ? (<>
							<div>{discordUser?.global_name || "NA"}</div>
							<div className="text-sm">{websiteUser?.email || "NA"}</div>
						</>) : (<>
							<Spinner size="small"/>
							<Spinner size="small"/>
						</>)
						}
					</div>
					<Avatar className="ml-2 mt-1 w-8 h-8">
						<AvatarImage src={discordUser?.profile_picture || ''}/>
						<AvatarFallback>
							<Spinner size="medium"/>
						</AvatarFallback>
					</Avatar>
				</div>
			</div>
			<div className="flex-grow overflow-auto">
				{children}
			</div>
		</div>
	);
};

export default BaseLayout;