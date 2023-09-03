<script>
	import TableViewPage from '../../comonents/list-view/TableViewPage.svelte';
	import { API_REJECTED_PROJECT, API_REJECTED_PROJECT_DESCRIPTION } from '$lib/consts';
</script>

<TableViewPage description_url={API_REJECTED_PROJECT_DESCRIPTION} api_url={API_REJECTED_PROJECT} />
