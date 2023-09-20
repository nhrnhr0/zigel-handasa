<script>
	import CurrencyCell from '../currencyCell.svelte';

	export let data;
	let total_recipts = 0;
	let total_invoices = data.row.total_before_tax;
	$: {
		if (data) {
			let childs = data.row.childs;
			total_recipts = childs.reduce((acc, curr) => acc + parseFloat(curr.rel_total), 0);
		}
	}
	let prc = ((parseInt(total_recipts) / parseInt()) * 100).toFixed(0);
</script>

<td>
	<CurrencyCell data={total_recipts} />

	<!-- progress bar from total_recipts out of totak_invoices  -->
	<div class="progress" role="progressbar" style="width: 100%;">
		<div class="progress-bar" style="width: {((total_recipts / total_invoices) * 100).toFixed(0)}%">
			{((total_recipts / total_invoices) * 100).toFixed(0)}%
		</div>
	</div>
</td>
