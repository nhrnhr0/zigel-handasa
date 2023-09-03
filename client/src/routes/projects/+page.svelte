<script>
	import TableViewPage from '../../comonents/list-view/TableViewPage.svelte';
	import { API_PROJECTS, API_PROJECTS_DESCRIPTION } from '$lib/consts';
</script>

<TableViewPage description_url={API_PROJECTS_DESCRIPTION} api_url={API_PROJECTS} />
