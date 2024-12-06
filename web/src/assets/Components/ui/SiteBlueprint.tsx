import * as React from "react";
import {Avatar, AvatarFallback, AvatarImage} from "../ui/avatar";
import {useDiscordUser} from "../../../context/DiscordUserContext";

interface BaseLayoutProps {
	children: React.ReactNode;
}

const BaseLayout: React.FC<BaseLayoutProps> = ({children}) => {
	const {discordUser} = useDiscordUser();

	return (
		<div className="flex flex-col h-screen bg-gradient-to-b from-gray-900 to-gray-800">
			<div className="flex items-center justify-between p-2 bg-gray-800"
				 style={{height: '8%', minHeight: '50px'}}>
				<div className="flex items-center">
					<Avatar className="w-8 h-8">
						<AvatarImage src="/KVGG/KVGG Logo Icon.png"/>
						<AvatarFallback>KVGG Logo</AvatarFallback>
					</Avatar>
				</div>
				<div className="text-white text-3xl underline mx-auto flex items-center">
					KVGG
				</div>
				<div className="flex items-center">
					<Avatar>
						<AvatarImage src={discordUser?.profile_picture || ''}/>
						<AvatarFallback>NA</AvatarFallback>
					</Avatar>
					<div className="ml-2 text-white">
						<div>{discordUser?.global_name || "NA"}</div>
						<div className="text-sm">{discordUser?.global_name || "NA"}</div>
					</div>
				</div>
			</div>
			<div className="flex-grow">
				{children}
			</div>
		</div>
	);
};

export default BaseLayout;
