<script>
	export let data;
	let value = new Intl.NumberFormat('he-IL', {
		style: 'currency',
		currency: 'ILS',
		minimumFractionDigits: 2,
		maximumFractionDigits: 2
	}).format(data);
</script>

{value}
