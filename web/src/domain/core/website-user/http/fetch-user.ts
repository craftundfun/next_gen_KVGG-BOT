import type WebsiteUser from "../@types/website-user.ts";

async function fetchUser(): Promise<WebsiteUser> {
	const response = await fetch('/api/websiteUser/me', {
		method: 'GET',
		credentials: 'include',
		headers: {
			'Content-Type': 'application/json',
		}
	});

	if (!response.ok) {
		throw new Error('Network response was not ok');
	}

	const data: unknown = await response.json();

	if (!data) {
		throw new Error('No user data found');
	}

	return data as WebsiteUser;
}

export default fetchUser;