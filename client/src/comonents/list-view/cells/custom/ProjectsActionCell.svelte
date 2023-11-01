<script>
	import ActionDropdown from '../../../shered/ActionDropdown.svelte';
	import { goto } from '$app/navigation';

	export let data;

	function go_to_project() {
		window.location.href = `/projects/${data.row.id}`;
	}

	function action_clicked_callback(e) {
		console.log(e); //
		if (e.detail == 'הפק חשבונית חדשה') {
			// goto /accounting/new/invoice?linkedDocumentIds=<morning_id>
			let morning_id = data.row.morning_id;
			goto(`/accounting/new/invoice?linkedDocumentIds=${morning_id}`);
		}
	}
</script>

<td>
	<ul class="list-inline m-0">
		<li class="list-inline-item">
			<!-- edit -->

			<button
				on:click={go_to_project}
				class="btn btn-secondary btn-sm rounded-0"
				type="button"
				data-toggle="tooltip"
				data-placement="top"
				title="Edit"><i class="fa fa-edit" /></button
			>
			<!-- new invoice -->
			<ActionDropdown actions={['הפק חשבונית חדשה']} on:action_clicked={action_clicked_callback} />
		</li>
	</ul>
</td>

<style lang="scss">
	ul.list-inline {
		padding: 0px;
		.list-inline-item {
			padding: 0px;
			margin: 0px;
			display: flex;
			justify-content: space-around;
			align-items: center;
			flex-direction: row;
		}
	}
</style>
