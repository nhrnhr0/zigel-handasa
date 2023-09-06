<!-- <script>
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
{/if} -->

<script>
	import { page } from '$app/stores';
	import { network_update_project } from '$lib/network.js';
	import EditProject from '../../../comonents/EditProject.svelte';
	// export let data;
	import { beforeNavigate } from '$app/navigation';
	import { onMount } from 'svelte';
	import { API_PROJECTS } from '$lib/consts';

	let form_data = undefined;
	let original_data = undefined;

	onMount(async () => {
		let url = `${API_PROJECTS}${$page.params.id}/`;
		console.log('fetching awaiting project data from server', url);
		const res = await fetch(url);
		const data = await res.json();
		original_data = JSON.parse(JSON.stringify(data));
		form_data = JSON.parse(JSON.stringify(data));
	});

	async function update_project(project_id, p_data) {
		const res = await network_update_project(project_id, p_data);
		console.log('res: ', res);
		if (res.status == 200) {
			alert('הפרויקט עודכן בהצלחה');
			form_data = JSON.parse(JSON.stringify(p_data));
			original_data = JSON.parse(JSON.stringify(p_data));
		}
		return res;
	}

	// beforeNavigate we check if form_data is diffrent from data.project_data (the original data)
	// if it is diffrent we ask the user if he wants to save the changes
	// if he does we call update_project
	// if he doesn't we just navigate to the new page
	beforeNavigate(async ({ to, cancel }) => {
		if (JSON.stringify(form_data) != JSON.stringify(original_data)) {
			if (confirm('האם ברצונך לשמור את השינויים?')) {
				// save the changes
				const res = await update_project(form_data.id, form_data);
				if (res.status == 200) {
					return true;
				} else {
					return false;
				}
			} else {
				// don't save the changes
				return true;
			}
		} else {
			// no changes
			return true;
		}
	});
</script>

{#if form_data}
	<EditProject bind:form_data on_update_function={update_project} />
{/if}

<style lang="scss">
</style>
