<script>
	import { API_PROJECTS } from '$lib/consts';
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { MultiSelect } from 'svelte-multiselect';
	import { network_update_project } from '$lib/network.js';
	let project_data = undefined;
	let name = undefined;
	let client = undefined;
	let client_options = undefined;
	let sum = undefined;
	let created_at = undefined;
	let updated_at = undefined;
	let status = undefined;
	let status_options = undefined;
	let order_number = undefined;
	let loaded = false;
	function update_project() {
		network_update_project(project_data.id, {
			name: name,
			client: client[0].value,
			total: sum,
			status: status,
			order_number: order_number
		}).then((res) => {
			console.log('res: ', res);
			if (res.status == 200) {
				alert('הפרויקט עודכן בהצלחה');
			}
		});
	}
	onMount(async () => {
		debugger;
		let url = `${API_PROJECTS}${$page.params.id}/`;
		console.log('fetching awaiting project data from server', url);
		const res = await fetch(url);
		const data = await res.json();
		// return data to be passed to page
		project_data = data;
		name = data.name;

		sum = data.total;
		created_at = data.created_at;
		updated_at = data.updated_at;

		order_number = data.order_number;
		client_options = data.client_options;
		status_options = data.status_options;

		client = client_options.filter((option) => option.value == data.client);
		status = status_options.filter((option) => option.value == data.status);
		loaded = true;
	});
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
			<label for="order_number">מספר הזמנה</label>
			<input type="text" class="form-control" id="order_number" bind:value={order_number} />
		</div>
		<div class="form-group">
			<label for="status">סטטוס</label>
			<MultiSelect
				options={status_options}
				maxSelect={1}
				bind:selected={status}
				allowUserOptions={true}
				createOptionMsg={'הוסף סטטוס חדש'}
			/>
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
{/if}
