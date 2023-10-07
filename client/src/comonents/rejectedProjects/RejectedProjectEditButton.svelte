<script>
	import { goto } from '$app/navigation';
	export let data;
	function go_to_rejected_project() {
		goto(`/rejected-project/${data.row.id}`);
	}
</script>

<td>
	<button
		on:click={go_to_rejected_project}
		class="btn btn-secondary btn-sm rounded-0"
		type="button"
		data-toggle="tooltip"
		data-placement="top"
		title="Edit"><i class="fa fa-edit" /></button
	>
</td>
