<script>
	import { API_REJECTED_PROJECT, API_REJECTED_PROJECT_DESCRIPTION } from '$lib/consts';
	import { onMount } from 'svelte';
	import ProjectsListView from '../../comonents/list-view/ProjectsListView.svelte';
	import TableDataPanel from '../../comonents/list-view/panels/TableDataPanel.svelte';
	import TableFilterPanel from '../../comonents/list-view/panels/TableFilterPanel.svelte';
	import RejectedProjectApproveButton from '../../comonents/rejectedProjects/RejectedProjectApproveButton.svelte';
	let description_url = API_REJECTED_PROJECT_DESCRIPTION;
	let api_url = API_REJECTED_PROJECT;
	let description_data = undefined;
	let api_data = undefined;
	let allow_select = false;
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
	let custom_components = {
		'rejected-project-approve-button': RejectedProjectApproveButton
	};
</script>

<!-- TODOO -->
<!-- <ProjectsListView {description_url} {api_url} /> -->
<div class="wraper">
	<div class="row">
		{#if description_data && api_data}
			<TableFilterPanel description={description_data} {api_data} />
			<TableDataPanel
				description={description_data}
				{api_data}
				{allow_select}
				user_cell_components={custom_components}
			/>
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
