<script>
	import TableViewPage from '../../comonents/list-view/TableViewPage.svelte';
	import { API_PROJECTS, API_PROJECTS_DESCRIPTION } from '$lib/consts';
	import { onMount } from 'svelte';
	let description_url = API_PROJECTS_DESCRIPTION;
	let api_url = API_PROJECTS;
	let description_data = undefined;
	let api_data = undefined;
	onMount(async () => {
		console.log('awaiting projects page');
		// fetch description
		fetchDescription();
		fetchApiData();
	});

	const fetchDescription = async () => {
		const res = await fetch(description_url);
		description_data = await res.json();
	};

	const fetchApiData = async () => {
		// add our filters (query params) to the url
		let url = api_url + window.location.search;
		const res = await fetch(url);
		api_data = await res.json();
	};
</script>

{#if description_data && api_data}
	<TableViewPage {description_data} {api_data} />
{/if}
