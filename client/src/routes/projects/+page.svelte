<script>
	import { API_PROJECTS, API_PROJECTS_DESCRIPTION } from '$lib/consts';

	import ProjectsListView from '../../comonents/list-view/ProjectsListView.svelte';
	let description_url = API_PROJECTS_DESCRIPTION;
	let api_url = API_PROJECTS;
</script>

<ProjectsListView {description_url} {api_url} />

<!-- <script>
	import { API_PROJECTS, API_PROJECTS_DESCRIPTION } from '$lib/consts';
	import { network_get_project_accounting_docs } from '$lib/network.js';
	import { onMount } from 'svelte';
	import TableFilterPanel from '../../comonents/list-view/panels/TableFilterPanel.svelte';
	import TableDataPanel from '../../comonents/list-view/panels/TableDataPanel.svelte';
	import CurrencyCell from '../../comonents/list-view/cells/currencyCell.svelte';
	import HebrewDatetimeCell from '../../comonents/list-view/cells/HebrewDatetimeCell.svelte';
	import ToolTipComponent from '../../comonents/shered/ToolTipComponent.svelte';
	import RelatedDocsTable from '../../comonents/layout/RelatedDocsTable.svelte';
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
					<table class="table table-bordered">
						<thead>
							<tr>
								<th scope="col">תאריך</th>
								<th scope="col">מספר מסמך</th>
								<th scope="col">סוג</th>
								<th scope="col">סכום</th>
								<th scope="col">סה"כ חשבוניות לפני מע"מ</th>
							</tr>
						</thead>
						<tbody>
							{#if slots_data[row.id] != undefined}
								{#each slots_data[row.id] as doc, index}
									<tr>
										<td>
											<HebrewDatetimeCell data={doc.doc_date} />
										</td>
										<td>
											<ToolTipComponent>
												<a href="#" style="color: black;">
													<svg
														xmlns="http://www.w3.org/2000/svg"
														width="18"
														height="18"
														viewBox="0 0 24 24"
														><path
															d="M6.188 8.719c.439-.439.926-.801 1.444-1.087 2.887-1.591 6.589-.745 8.445 2.069l-2.246 2.245c-.644-1.469-2.243-2.305-3.834-1.949-.599.134-1.168.433-1.633.898l-4.304 4.306c-1.307 1.307-1.307 3.433 0 4.74 1.307 1.307 3.433 1.307 4.74 0l1.327-1.327c1.207.479 2.501.67 3.779.575l-2.929 2.929c-2.511 2.511-6.582 2.511-9.093 0s-2.511-6.582 0-9.093l4.304-4.306zm6.836-6.836l-2.929 2.929c1.277-.096 2.572.096 3.779.574l1.326-1.326c1.307-1.307 3.433-1.307 4.74 0 1.307 1.307 1.307 3.433 0 4.74l-4.305 4.305c-1.311 1.311-3.44 1.3-4.74 0-.303-.303-.564-.68-.727-1.051l-2.246 2.245c.236.358.481.667.796.982.812.812 1.846 1.417 3.036 1.704 1.542.371 3.194.166 4.613-.617.518-.286 1.005-.648 1.444-1.087l4.304-4.305c2.512-2.511 2.512-6.582.001-9.093-2.511-2.51-6.581-2.51-9.092 0z"
														/></svg
													>
													{doc.doc_number}
												</a>
												<div slot="content">
													<RelatedDocsTable related_docs={doc.related_docs} />
												</div>
											</ToolTipComponent>
										</td>
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
			</div>
		</TableDataPanel>
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
</style> -->
