<script>
	import CurrencyCell from '../currencyCell.svelte';
	import { tooltip } from '../../../shered/tooltip';
	import ProgressBar from '@okrad/svelte-progressbar';
	import { onMount } from 'svelte';
	export let data;
	// let title = `סכום פתוח: ${new Intl.NumberFormat('he-IL', {
	// 	style: 'currency',
	// 	currency: 'ILS',
	// 	minimumFractionDigits: 2,
	// 	maximumFractionDigits: 2
	// }).format(parseInt(data.row.total_before_tax) - parseInt(data.row.total_invoices_before_tax))}`;
	let intl = new Intl.NumberFormat('he-IL', {
		style: 'currency',
		currency: 'ILS',
		minimumFractionDigits: 0,
		maximumFractionDigits: 2
	});

	let open_total =
		parseInt(data.row.total_before_tax) - parseInt(data.row.total_invoices_before_tax);
	let current_total = parseInt(data.row.total_invoices_before_tax);
	let total = parseInt(data.row.total_before_tax);
	let title = `${intl.format(current_total)} מתוך ${intl.format(total)}`;

	let total_progress =
		(parseInt(data.row.total_invoices_before_tax) / parseInt(data.row.total_before_tax)) * 100;
</script>

<!-- data.row.total_invoices_before_tax out of data.row.total_before_tax  -->

<!-- example:<div class="progress" role="progressbar" aria-label="Basic example" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100">
  <div class="progress-bar" style="width: 25%"></div>
</div>
    -->
<td>
	<div class="tooltip-wraper" {title} use:tooltip style="width:100%;">
		<div class="progress" role="progressbar" style="width: 100%;">
			<div class="progress-bar" style="width: {total_progress}%">
				{(
					(parseInt(data.row.total_invoices_before_tax) / parseInt(data.row.total_before_tax)) *
					100
				).toFixed(0)}%
				<!-- <CurrencyCell data={parseInt(data.row.total_invoices_before_tax)} /> -->
			</div>
		</div>
	</div>
</td>
<!-- <div id="progress-bar-{data.row.id}" style="width: 100%;" use:tooltip {title} /> -->
