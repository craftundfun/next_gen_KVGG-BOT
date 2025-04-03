export async function customFetch(url: string, options = {}) {
	const response = await fetch(url, options);

	if (response.status === 401) {
		window.location.href = "/forbidden";
	}

	return response;
}
