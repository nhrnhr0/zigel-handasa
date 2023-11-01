<script>
	import ToolTipComponent from '../../../shered/ToolTipComponent.svelte';
	import { tooltip } from '../../../shered/tooltip';
	import HebrewDatetimeCell from '../HebrewDatetimeCell.svelte';
	import CurrencyCell from '../currencyCell.svelte';

	export let data;
	let len = data['description']['api-description'].max_childs_count;

	let row = data.row;
	let recipts = row.childs.filter((child) => child.type == 'קבלה');
</script>

{#each { length: len } as _, i}
	<td>
		{#if recipts.length > i}
			<div
				use:tooltip
				title={new Date(recipts[i].doc_date).toLocaleDateString('he-IL', {
					timeZone: 'Asia/Jerusalem'
				}) +
					' (' +
					recipts[i].doc_number +
					')'}
			>
				<CurrencyCell data={recipts[i].rel_total} />
				{#if recipts[i].rel_total != recipts[i].total}
					מתוך <CurrencyCell data={recipts[i].total} />
				{/if}
			</div>
		{/if}
	</td>
{/each}
