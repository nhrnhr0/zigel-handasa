<script>
	import { page } from '$app/stores';
	import { network_update_awaiting_project } from '$lib/network.js';
	import EditProject from '../../../comonents/EditProject.svelte';
	export let data;
	import { beforeNavigate } from '$app/navigation';
	let form_data = JSON.parse(JSON.stringify(data.project_data));
	async function update_project(project_id, p_data) {
		// console.log('update_project');
		// console.log('name: ', name);
		// console.log('client: ', client);
		// console.log('sum: ', sum);
		// console.log('created_at: ', created_at);
		// console.log('updated_at: ', updated_at);
		// console.log('loaded: ', loaded);
		// console.log('data.project_data: ', data.project_data);
		// console.log('client_options: ', client_options);

		// put to `${API_AWAITING_PROJECTS}${params.id}/`;
		const res = await network_update_awaiting_project(project_id, p_data);
		console.log('res: ', res);
		if (res.status == 200) {
			alert('הפרויקט עודכן בהצלחה');
			data.project_data = JSON.parse(JSON.stringify(p_data));
		}
		return res;
	}

	// beforeNavigate we check if form_data is diffrent from data.project_data (the original data)
	// if it is diffrent we ask the user if he wants to save the changes
	// if he does we call update_project
	// if he doesn't we just navigate to the new page
	beforeNavigate(async ({ to, cancel }) => {
		debugger;
		if (JSON.stringify(form_data) != JSON.stringify(data.project_data)) {
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

<EditProject bind:form_data on_update_function={update_project} />

<!-- {#if loaded}
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
	</form> -->

<!-- page actions: 2 buttons
	רלוונטי
	לא רלוונטי
	-->
<!-- <div class="page-actions">
	<div class="buttons-wraper">
		<button type="button" class="btn btn-success" on:click={handleApproveClick}> סמן כאושר </button>
		<button type="button" class="btn btn-danger" on:click={handleRejectClick}> סמן כנדחה </button>
	</div>
</div> -->

<!-- {/if} -->

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
