<script>
	import TableViewPage from '../../comonents/list-view/TableViewPage.svelte';
	import { API_ACCOUNTING_DOCS, API_ACCOUNTING_DOCS_DESCRIPTION } from '$lib/consts';
	import BulkActions from '../../comonents/list-view/compontnts/BulkActions.svelte';
	let selected_ids = [];
	let selected_data = [];
	let api_data = undefined;

	let actions = [];
	function on_select_change(selected_ids_dict, selected_data) {
		debugger;
		if (selected_data.length == 0) {
			actions = [];
			return;
		} else {
			actions = [
				{
					label: 'הורד',
					action: () => {
						console.log('download');
					}
				}
			];
		}

		// if only price proposals are selected, and they are all from the same client, add actions: create invoice and create receipt
		// if only invoices are selected, and they are all from the same client, add actions: create receipt
		// if only receipts are selected, and they are all from the same client, add actions: create invoice

		let only_price_proposals_selected = true;
		let only_invoices_selected = true;
		let only_receipts_selected = true;
		let only_one_client_selected = true;
		let selected_client = undefined;
		debugger;
		for (const row of selected_data) {
			if (row.type != 'הצעת מחיר') {
				only_price_proposals_selected = false;
			}
			if (row.type != 'חשבונית') {
				only_invoices_selected = false;
			}
			if (row.type != 'קבלה') {
				only_receipts_selected = false;
			}
			if (selected_client == undefined) {
				selected_client = row.client__name;
			} else {
				if (selected_client != row.client__name) {
					only_one_client_selected = false;
				}
			}
		}
		debugger;
		if (only_price_proposals_selected && only_one_client_selected) {
			actions.push({
				label: 'צור חשבונית',
				action: () => {
					console.log('create invoice');
				}
			});
			actions.push({
				label: 'צור קבלה',
				action: () => {
					console.log('create receipt');
				}
			});
		}

		if (only_invoices_selected && only_one_client_selected) {
			actions.push({
				label: 'צור קבלה',
				action: () => {
					console.log('create receipt');
				}
			});
		}

		if (only_receipts_selected && only_one_client_selected) {
			actions.push({
				label: 'צור חשבונית',
				action: () => {
					console.log('create invoice');
				}
			});
		}
		actions = [...actions];
	}
</script>

<TableViewPage
	description_url={API_ACCOUNTING_DOCS_DESCRIPTION}
	api_url={API_ACCOUNTING_DOCS}
	bind:api_data
	allow_select={true}
	{on_select_change}
	bind:actions
/>
<!-- {#if selected_ids}
	{#each Object.keys(selected_ids) as id}
		<p>{id}</p>
	{/each}
{/if} -->
