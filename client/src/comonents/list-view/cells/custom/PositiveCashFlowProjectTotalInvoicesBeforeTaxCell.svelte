<script>
	import CurrencyCell from '../currencyCell.svelte';
	import { convert_to_money, get_hebrew_date, get_hebrew_datetime } from '$lib/utils.js';
	import { tooltip } from '../../../shered/tooltip';
	export let data;
	let row = data.row;
	let prc = (
		(parseInt(row.total_invoices_before_tax) / parseInt(row.root_price_proposal__total)) *
		100
	).toFixed(0);
</script>

<td>
	{convert_to_money(row.total_invoices_before_tax)}
	<div
		class="progress"
		role="progressbar"
		style="width: 100%;"
		use:tooltip
		title="{convert_to_money(row.total_invoices_before_tax)} מתוך {convert_to_money(
			row.root_price_proposal__total_before_tax
		)}"
	>
		<div class="progress-bar" style="width: {prc}%">
			{prc}%
		</div>
	</div>
</td>
