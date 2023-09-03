<script>
	import TableViewPage from '../../comonents/list-view/TableViewPage.svelte';
	import { API_AWAITING_PROJECTS_DESCRIPTION, API_AWAITING_PROJECTS } from '$lib/consts';
</script>

<TableViewPage
	description_url={API_AWAITING_PROJECTS_DESCRIPTION}
	api_url={API_AWAITING_PROJECTS}
/>
