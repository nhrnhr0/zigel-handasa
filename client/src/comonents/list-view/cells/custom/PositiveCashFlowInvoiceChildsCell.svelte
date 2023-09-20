<script>
	import ToolTipComponent from '../../../shered/ToolTipComponent.svelte';
	import { tooltip } from '../../../shered/tooltip';
	import HebrewDatetimeCell from '../HebrewDatetimeCell.svelte';
	import CurrencyCell from '../currencyCell.svelte';

	export let data;
	let len = data['description']['api-description'].max_childs_count;
	let row = data.row;
</script>

{#each { length: len } as _, i}
	<td>
		{#if row.childs.length > i}
			<!-- <ToolTipComponent>
				<CurrencyCell data={row.childs[i].rel_total} />
				<div slot="content">
					<table class="table table-bordered">
						<thead>
							<tr>
								<th scope="col">תאריך</th>
								<th scope="col">סכום</th>
								<th scope="col">מספר מסמך</th>
							</tr>
						</thead>
						<tbody>
							<tr>
								<td>
									<HebrewDatetimeCell data={row.childs[i].doc_date} />
								</td>
								<td>
									<CurrencyCell data={row.childs[i].rel_total} />
									{#if row.childs[i].rel_total != row.childs[i].total}
										מתוך <CurrencyCell data={row.childs[i].total} />
									{/if}
								</td>
								<td>
									{row.childs[i].doc_number}
								</td>
							</tr>
						</tbody>
					</table>
				</div>
			</ToolTipComponent> -->
			<div
				use:tooltip
				title={new Date(row.childs[i].doc_date).toLocaleDateString('he-IL', {
					timeZone: 'Asia/Jerusalem'
				}) +
					' (' +
					row.childs[i].doc_number +
					')'}
			>
				<CurrencyCell data={row.childs[i].rel_total} />
				{#if row.childs[i].rel_total != row.childs[i].total}
					מתוך <CurrencyCell data={row.childs[i].total} />
				{/if}
			</div>
		{/if}
	</td>
{/each}
