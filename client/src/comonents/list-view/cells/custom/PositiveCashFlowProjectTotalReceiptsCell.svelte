<script>
	import CurrencyCell from '../currencyCell.svelte';
	import { convert_to_money, get_hebrew_date, get_hebrew_datetime } from '$lib/utils.js';
	import { tooltip } from '../../../shered/tooltip';

	export let data;
	let row = data.row;
	let total_recipts = row.recipts.reduce((acc, curr) => acc + parseFloat(curr.rel_total), 0);
	let total_total = row.total_invoices_before_tax || 1;
</script>

{#if data}
	<td>
		{convert_to_money(total_recipts)}
		<div
			class="progress"
			role="progressbar"
			style="width: 100%;"
			use:tooltip
			title="{convert_to_money(total_recipts)} מתוך {convert_to_money(total_total)}"
		>
			<div class="progress-bar" style="width: {((total_recipts / total_total) * 100).toFixed(0)}%">
				{((total_recipts / total_total) * 100).toFixed(0)}%
			</div>
		</div>
	</td>
{/if}
