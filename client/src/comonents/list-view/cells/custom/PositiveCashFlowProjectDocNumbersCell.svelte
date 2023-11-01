<script>
	import { tooltip } from '../../../shered/tooltip';
	import { convert_to_money, get_hebrew_date } from '$lib/utils.js';
	export let data;
</script>

<td>
	<div class="doc-numbers">
		{#each data.row.doc_numbers as doc}
			<div
				class="doc-number"
				use:tooltip
				title={'' +
					get_hebrew_date(doc.doc_date) +
					' (' +
					convert_to_money(doc.total_before_tax) +
					')'}
			>
				{doc.doc_number}
			</div>
		{/each}
	</div>
</td>

<style lang="scss">
	.doc-numbers {
		display: flex;
		flex-wrap: wrap;
		gap: 5px;
	}
	.doc-number {
		display: inline-block;
		// margin: 0 5px;
		padding: 0 5px;
		background-color: #cecece;
		border-radius: 5px;
	}
</style>
