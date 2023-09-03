<script>
	import TableViewPage from '../../comonents/list-view/TableViewPage.svelte';
	import { API_ACCOUNTING_DOCS, API_ACCOUNTING_DOCS_DESCRIPTION } from '$lib/consts';
</script>

<TableViewPage description_url={API_ACCOUNTING_DOCS_DESCRIPTION} api_url={API_ACCOUNTING_DOCS} />
