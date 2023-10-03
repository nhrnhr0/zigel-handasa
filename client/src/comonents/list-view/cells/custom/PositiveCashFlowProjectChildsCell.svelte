<script>
	import { convert_to_money, get_hebrew_date, get_hebrew_datetime } from '$lib/utils.js';
	import ToolTipComponent from '../../../shered/ToolTipComponent.svelte';
	import { tooltip } from '../../../shered/tooltip';
	import CurrencyCell from '../currencyCell.svelte';

	export let data;
	let len = data['description']['api-description'].max_childs_count;

	let recipts = data.row.recipts;
</script>

{#each { length: len } as _, i}
	<td>
		{#if recipts.length > i}
			<div
				use:tooltip
				title={get_hebrew_date(recipts[i]?.doc_date) + ' (' + recipts[i]?.doc_number + ')'}
			>
				<CurrencyCell data={recipts[i].rel_total} />
			</div>
		{/if}
	</td>
{/each}
