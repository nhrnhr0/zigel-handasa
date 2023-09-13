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
	let title =
		(
			(parseInt(data.row.total_invoices_before_tax) / parseInt(data.row.total_before_tax)) *
			100
		).toFixed(0) +
		'% (נותר לחייב ' +
		new Intl.NumberFormat('he-IL', {
			style: 'currency',
			currency: 'ILS',
			minimumFractionDigits: 0,
			maximumFractionDigits: 2
		}).format(parseInt(data.row.total_before_tax) - parseInt(data.row.total_invoices_before_tax)) +
		')';
	let total_progress =
		(parseInt(data.row.total_invoices_before_tax) / parseInt(data.row.total_before_tax)) * 100;
	onMount(() => {
		// let prc =
		// 	(parseInt(data.row.total_invoices_before_tax) / parseInt(data.row.total_before_tax)) * 100;
		// new ProgressBar({
		// 	target: document.getElementById(`progress-bar-${data.row.id}`),
		// 	props: {
		// 		style: 'thin',
		// 		series: [prc],
		// 		color: '#007bff'
		// 	}
		// });
	});
</script>

<!-- data.row.total_invoices_before_tax out of data.row.total_before_tax  -->

<!-- example:<div class="progress" role="progressbar" aria-label="Basic example" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100">
  <div class="progress-bar" style="width: 25%"></div>
</div>
    -->
<div class="tooltip-wraper" {title} use:tooltip style="width:100%;">
	<div class="progress" role="progressbar" style="width: 100%;">
		<div class="progress-bar" style="width: {total_progress}%">
			<CurrencyCell data={parseInt(data.row.total_invoices_before_tax)} />
		</div>
	</div>
</div>
<!-- <div id="progress-bar-{data.row.id}" style="width: 100%;" use:tooltip {title} /> -->
