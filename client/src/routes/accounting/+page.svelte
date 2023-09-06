<script>
	import TableViewPage from '../../comonents/list-view/TableViewPage.svelte';
	import { API_ACCOUNTING_DOCS, API_ACCOUNTING_DOCS_DESCRIPTION } from '$lib/consts';
	import { goto } from '$app/navigation';
	let api_data = undefined;

	function create_invoice(docs) {
		// goto new invoice page with docs ids in query params linkedDocumentIds=['morning_id1',...]
		let url = '/accounting/new/invoice/?linkedDocumentIds=';
		debugger;
		for (const doc of docs) {
			url += doc.morning_id + ',';
		}
		url = url.slice(0, -1);
		console.log('url: ', url);
		goto(url);
	}

	let actions = [];
	function on_select_change(selected_ids_dict, selected_data) {
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
		if (only_price_proposals_selected && only_one_client_selected) {
			actions.push({
				label: 'צור חשבונית על סמך הצעות מחיר',
				action: () => {
					create_invoice(selected_data);
				}
			});
			actions.push({
				label: 'צור קבלה על סמך הצעות מחיר',
				action: () => {
					create_receipt(selected_data);
				}
			});
		}

		if (only_invoices_selected && only_one_client_selected) {
			actions.push({
				label: 'צור קבלה על סמך חשבונית',
				action: () => {
					create_receipt(selected_data);
				}
			});
		}

		if (only_receipts_selected && only_one_client_selected) {
			actions.push({
				label: 'צור חשבונית על סמך קבלות',
				action: () => {
					create_invoice(selected_data);
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
