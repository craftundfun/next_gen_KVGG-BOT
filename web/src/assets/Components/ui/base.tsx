import * as React from "react";
import {Avatar, AvatarFallback, AvatarImage} from "../ui/avatar";

interface BaseLayoutProps {
	children: React.ReactNode;
}

const BaseLayout: React.FC<BaseLayoutProps> = ({children}) => {
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
					<button className="text-white">
						<svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"
							 xmlns="http://www.w3.org/2000/svg">
							<path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"
								  d="M4 6h16M4 12h16m-7 6h7"></path>
						</svg>
					</button>
				</div>
			</div>
			<div className="flex-grow">
				{children}
			</div>
		</div>
	);
};

export default BaseLayout;