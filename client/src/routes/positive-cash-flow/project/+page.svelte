<script>
	import TableDataPanel from '../../../comonents/list-view/panels/TableDataPanel.svelte';
	import TableFilterPanel from '../../../comonents/list-view/panels/TableFilterPanel.svelte';
	import { API_POSITIVE_CASH_FLOW_PORJECTS } from '$lib/consts.js';
	import { onMount } from 'svelte';
	import PositiveCashFlowInvoiceChildsCell from '../../../comonents/list-view/cells/custom/PositiveCashFlowInvoiceChildsCell.svelte';
	import PositiveCashFlowInvoiceTotalReceiptsCell from '../../../comonents/list-view/cells/custom/PositiveCashFlowInvoiceTotalReceiptsCell.svelte';
	import PositiveCashFlowProjectChildsCell from '../../../comonents/list-view/cells/custom/PositiveCashFlowProjectChildsCell.svelte';
	import PositiveCashFlowProjectDocNumbersCell from '../../../comonents/list-view/cells/custom/PositiveCashFlowProjectDocNumbersCell.svelte';
	import PositiveCashFlowProjectTotalReceiptsCell from '../../../comonents/list-view/cells/custom/PositiveCashFlowProjectTotalReceiptsCell.svelte';
	import PositiveCashFlowProjectTotalInvoicesBeforeTaxCell from '../../../comonents/list-view/cells/custom/PositiveCashFlowProjectTotalInvoicesBeforeTaxCell.svelte';
	let api_url = API_POSITIVE_CASH_FLOW_PORJECTS;
	let description_data = undefined;
	let api_data = undefined;
	let allow_select = false;

	onMount(async () => {
		fetchApiData();
	});

	const fetchApiData = async () => {
		// add our filters (query params) to the url
		let url = api_url + window.location.search;
		const res = await fetch(url);
		api_data = await res.json();
		description_data = api_data['description'];
	};
	let user_cell_components = {
		'positive-cash-flow-project-doc-numbers': PositiveCashFlowProjectDocNumbersCell,
		'positive-cash-flow-project-childs': PositiveCashFlowProjectChildsCell,
		'positive-cash-flow-project-total-receipts': PositiveCashFlowProjectTotalReceiptsCell,
		'positive-cash-flow-project-total-invoices-before-tax':
			PositiveCashFlowProjectTotalInvoicesBeforeTaxCell
	};
</script>

<div class="wraper">
	<div class="row">
		{#if description_data && api_data}
			<TableFilterPanel description={description_data} {api_data} />
			<TableDataPanel
				description={description_data}
				{api_data}
				{allow_select}
				{user_cell_components}
				custom_height="calc(100vh - 350px)"
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
