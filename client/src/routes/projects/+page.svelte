<script>
	import TableViewPage from '../../comonents/list-view/TableViewPage.svelte';
	import { API_PROJECTS, API_PROJECTS_DESCRIPTION } from '$lib/consts';
	import { network_get_project_accounting_docs } from '$lib/network.js';
	import { onMount } from 'svelte';
	import TableFilterPanel from '../../comonents/list-view/panels/TableFilterPanel.svelte';
	import TableDataPanel from '../../comonents/list-view/panels/TableDataPanel.svelte';
	import CurrencyCell from '../../comonents/list-view/cells/currencyCell.svelte';
	import HebrewDatetimeCell from '../../comonents/list-view/cells/HebrewDatetimeCell.svelte';
	let description_url = API_PROJECTS_DESCRIPTION;
	let api_url = API_PROJECTS;
	let description_data = undefined;
	let api_data = undefined;
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
	let slots_data = {};

	function calculate_open_total(docs, index) {
		let total = 0;
		for (let i = 0; i <= index; i++) {
			total += parseFloat(docs[i].total);
		}
		return total;
	}
</script>

<div class="wraper">
	<div class="row">
		<TableFilterPanel description={description_data} {api_data} />
		<TableDataPanel
			description={description_data}
			{api_data}
			allow_select={false}
			expendable={true}
			on:expended_row_click={(e) => {
				console.log('expended_row_click', e.detail);
				if (e.detail.expended === true) {
					if (slots_data[e.detail.row.id] == undefined) {
						network_get_project_accounting_docs(e.detail.row.id).then((res) => {
							res.json().then((data) => {
								slots_data[e.detail.row.id] = data;
								console.log('slots_data', slots_data);
							});
						});
					}
				}
			}}
		>
			<div slot="expended-row-content" let:row let:row_index let:show>
				<div class="expended-content">
					<!-- תאריך
					מספר מסמך (קישור לטבלת קישורים ליד)
				סוג
			סכום
		סה"כ פתוח
	ת לתשלום -->
					<table class="table table-bordered">
						<thead>
							<tr>
								<th scope="col">תאריך</th>
								<th scope="col">מספר מסמך</th>
								<th scope="col">סוג</th>
								<th scope="col">סכום</th>
								<th scope="col">סה"כ חשבוניות לפני מע"מ</th>
								<!-- <th scope="col">תאריך לתשלום</th> -->
							</tr>
						</thead>
						<tbody>
							{#if slots_data[row.id] != undefined}
								{#each slots_data[row.id] as doc, index}
									<tr>
										<!-- doc_date,doc_number,type,total,'', -->
										<td>
											<HebrewDatetimeCell data={doc.doc_date} />
										</td>
										<td>{doc.doc_number}</td>
										<td>{doc.type}</td>
										<td>
											<CurrencyCell data={doc.total} />
											{#if doc.child_total != doc.total}
												(מתוך:
												<CurrencyCell data={doc.child_total} />)
											{/if}
										</td>
										<td
											><CurrencyCell data={calculate_open_total(slots_data[row.id], index)} />
										</td>
									</tr>
								{/each}
							{:else}
								<tr>
									<td colspan="5">טוען...</td>
								</tr>
							{/if}
						</tbody>
					</table>
				</div>
			</div></TableDataPanel
		>
	</div>
</div>

<style lang="scss">
	.expended-content {
		background-color: #f5f5f5;
		padding: 10px;
	}
	.wraper {
		.row {
			margin: 0;
			padding: 0;
		}
	}
</style>
