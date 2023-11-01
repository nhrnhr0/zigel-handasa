<script>
	import TableViewPage from '../../comonents/list-view/TableViewPage.svelte';
	import { API_AWAITING_PROJECTS_DESCRIPTION, API_AWAITING_PROJECTS } from '$lib/consts';
	import { network_get_overdue_awaiting_projects } from '$lib/network.js';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import TableDataPanel from '../../comonents/list-view/panels/TableDataPanel.svelte';
	import TableFilterPanel from '../../comonents/list-view/panels/TableFilterPanel.svelte';
	let description_url = API_AWAITING_PROJECTS_DESCRIPTION;
	let api_url = API_AWAITING_PROJECTS;
	let description_data = undefined;
	let api_data = undefined;
	let overdue_awaiting_projects = undefined;
	let allow_select = false;
	onMount(async () => {
		let token=localStorage.getItem("token")
		console.log(token)
		if(token&&token!=undefined){
			console.log('awaiting projects page');
			// fetch description
			fetchDescription();
			fetchApiData();
			// fetch overdue projects
			const res = await network_get_overdue_awaiting_projects();
			overdue_awaiting_projects = await res.json();
		}
		else{
			goto("/login")
		}
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

{#if overdue_awaiting_projects && description_data && overdue_awaiting_projects.results.length > 0}
	<!-- wanting card with the TableDataPanel -->
	<div class="alert alert-danger overdue-projects">
		<div class="overdue-projects-title">
			<h4>פרויקטים שדורשים טיפול מיידי:</h4>
		</div>
		<TableDataPanel
			description={description_data}
			api_data={overdue_awaiting_projects}
			allow_select={false}
			pagination={false}
			show_search_bar={false}
			custom_height="auto"
		/>
	</div>
{/if}
<div class="wraper">
	<div class="row">
		{#if description_data && api_data}
			<TableFilterPanel description={description_data} {api_data} />
			<TableDataPanel description={description_data} {api_data} {allow_select} />
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
	.overdue-projects {
		margin: 0.5rem;
		padding: 1rem;
		display: flex;
		justify-content: space-between;
		align-items: center;
		box-shadow: 0 0 10px 0 rgba(0, 0, 0, 0.2);

		.overdue-projects-title {
			background-color: #f5f5f5;
			padding: 0.5rem;
			border-radius: 5px;
		}
	}
</style>
