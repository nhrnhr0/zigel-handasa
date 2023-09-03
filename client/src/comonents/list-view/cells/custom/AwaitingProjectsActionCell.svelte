<script>
	import ModalApprove from '../../../../modals/awaiting-approval/ModalApprove.svelte';
	import ModalReject from '../../../../modals/awaiting-approval/ModalReject.svelte';
	import { openModal } from 'svelte-modals';

	export let data;

	function go_to_project() {
		window.location.href = `/waiting-approval/${data.row.id}`;
	}

	function handleApproveClick() {
		openModal(ModalApprove, { awaiting_project_id: data.row.id });
	}

	function handleRejectClick() {
		openModal(ModalReject, { awaiting_project_id: data.row.id });
	}
</script>

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

		<!-- reject -->
		<button
			on:click={handleRejectClick}
			class="btn btn-danger btn-sm rounded-0"
			type="button"
			data-toggle="tooltip"
			data-placement="top"
			title="Reject"><i class="fa fa-times" /></button
		>

		<!-- approve -->
		<button
			on:click={handleApproveClick}
			class="btn btn-success btn-sm rounded-0"
			type="button"
			data-toggle="tooltip"
			data-placement="top"
			title="Approve"><i class="fa fa-check" /></button
		>
	</li>
	<!-- <li class="list-inline-item">
		<button
			class="btn btn-danger btn-sm rounded-0"
			type="button"
			data-toggle="tooltip"
			data-placement="top"
			title="Delete"><i class="fa fa-trash" /></button
		>
	</li> -->
</ul>
