<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import MultiSelect from 'svelte-multiselect';
	import { network_update_awaiting_project } from '$lib/network.js';
	export let data;

	let name = undefined;
	let client = undefined;
	let client_options = undefined;
	let sum = undefined;
	let created_at = undefined;
	let updated_at = undefined;
	let loaded = false;

	onMount(() => {
		console.log('hey: ', data.project_data);
		name = data.project_data.name;
		client = [data.project_data.client];
		client_options = data.project_data.client_options;
		sum = data.project_data.total;
		created_at = data.project_data.created_at;
		updated_at = data.project_data.updated_at;
		loaded = true;
	});

	function update_project() {
		console.log('update_project');
		console.log('name: ', name);
		console.log('client: ', client);
		console.log('sum: ', sum);
		console.log('created_at: ', created_at);
		console.log('updated_at: ', updated_at);
		console.log('loaded: ', loaded);
		console.log('data.project_data: ', data.project_data);
		console.log('client_options: ', client_options);

		// put to `${API_AWAITING_PROJECTS}${params.id}/`;
		network_update_awaiting_project(data.project_data.id, {
			name: name,
			client: client[0].value,
			total: sum
		}).then((res) => {
			console.log('res: ', res);
			if (res.status == 200) {
				alert('הפרויקט עודכן בהצלחה');
			}
		});
	}

	import { openModal } from 'svelte-modals';
	import ModalApprove from '../../../modals/awaiting-approval/ModalApprove.svelte';
	import ModalReject from '../../../modals/awaiting-approval/ModalReject.svelte';
	function handleApproveClick() {
		openModal(ModalApprove, { awaiting_project_id: data.project_data.id });
	}

	function handleRejectClick() {
		openModal(ModalReject, { awaiting_project_id: data.project_data.id });
	}
</script>

{#if loaded}
	<form>
		<div class="form-group">
			<label for="name">שם</label>
			<input type="text" class="form-control" id="name" bind:value={name} />
		</div>
		<div class="form-group">
			<label for="client">לקוח</label>
			<MultiSelect options={client_options} maxSelect={1} bind:selected={client} />
		</div>
		<div class="form-group">
			<label for="sum">סכום</label>
			<input type="text" class="form-control" id="sum" bind:value={sum} />
		</div>
		<div class="form-group">
			<label for="created_at">נוצר בתאריך</label>
			{new Date(created_at).toLocaleString('he-IL', {
				timeZone: 'Asia/Jerusalem'
			})}
		</div>

		<div class="form-group">
			<label for="updated_at">עודכן לאחרונה</label>
			{new Date(updated_at).toLocaleString('he-IL', {
				timeZone: 'Asia/Jerusalem'
			})}
		</div>
		<button type="submit" class="btn btn-primary" on:click={update_project}>שמור</button>
	</form>

	<!-- page actions: 2 buttons
	רלוונטי
	לא רלוונטי
	-->
	<div class="page-actions">
		<div class="buttons-wraper">
			<button type="button" class="btn btn-success" on:click={handleApproveClick}>
				סמן כאושר
			</button>
			<button type="button" class="btn btn-danger" on:click={handleRejectClick}> סמן כנדחה </button>
		</div>
	</div>
{/if}

<style lang="scss">
	.page-actions {
		margin: auto;
		margin-top: 1rem;
		max-width: 300px;

		.buttons-wraper {
			display: flex;
			justify-content: space-between;
		}
	}
</style>
