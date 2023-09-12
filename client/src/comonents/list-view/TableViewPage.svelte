<script>
	import { onMount } from 'svelte';
	import TableFilterPanel from './panels/TableFilterPanel.svelte';
	import TableDataPanel from './panels/TableDataPanel.svelte';

	export let custom_height = undefined;

	export let allow_select = false;
	export let actions;

	export let description_data = undefined;
	export let api_data = undefined;

	export let on_select_change = undefined;
</script>

<!-- right panel with filters
    center panel with search bar and table
-->
<div class="wraper">
	<div class="row">
		{#if description_data && api_data}
			<TableFilterPanel description={description_data} {api_data} />
			<TableDataPanel
				description={description_data}
				{api_data}
				{allow_select}
				{on_select_change}
				{custom_height}
				bind:actions
			/>
		{/if}
	</div>
</div>

<style lang="scss">
	.wraper {
		.row {
			margin: 0;
			padding: 0;
		}
	}
</style>
