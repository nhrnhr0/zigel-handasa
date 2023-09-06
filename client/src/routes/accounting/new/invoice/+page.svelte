<script>
	import { onMount } from 'svelte';
	import { network_get_morning_info } from '$lib/network.js';
	// get linkedDocumentIds from the url query params
	let linkedDocumentIds = [];
	let data = undefined;
	onMount(async () => {
		let urlParams = new URLSearchParams(window.location.search);
		if (urlParams.has('linkedDocumentIds')) {
			linkedDocumentIds = urlParams.get('linkedDocumentIds').split(',');
		}
		debugger;
		data = await network_get_morning_info(linkedDocumentIds);
	});
</script>

<ul>
	{#each linkedDocumentIds as id}
		<li>{id}</li>
	{/each}
</ul>
