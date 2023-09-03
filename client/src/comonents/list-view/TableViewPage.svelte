<script>
	import { onMount } from 'svelte';
	import TableFilterPanel from './panels/TableFilterPanel.svelte';
	import TableDataPanel from './panels/TableDataPanel.svelte';

	export let description_url;
	export let api_url;

	let description_data = undefined;
	let api_data = undefined;

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

	onMount(async () => {
		fetchDescription();
		fetchApiData();
	});
</script>

<!-- right panel with filters
    center panel with search bar and table
-->
<div class="wraper">
	<div class="row">
		{#if description_data && api_data}
			<TableFilterPanel description={description_data} {api_data} />
			<TableDataPanel description={description_data} {api_data} />
		{/if}
	</div>
</div>

<style lang="scss">
	.wraper {
		.row {
			margin: 0;
			padding: 0;
		}
	}
</style>
