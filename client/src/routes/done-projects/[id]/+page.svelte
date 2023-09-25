<script>
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import { network_update_project } from '$lib/network.js';
	import EditProject from '../../../comonents/EditProject.svelte';
	// export let data;
	import { beforeNavigate } from '$app/navigation';
	import { onMount } from 'svelte';
	import { API_PROJECTS } from '$lib/consts';
	import { notifier } from '@beyonk/svelte-notifications';

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
		console.log('update_project', project_id, p_data);
		debugger;
		const res = await network_update_project(project_id, p_data);
		console.log('res: ', res);
		if (res.status == 200) {
			// alert('הפרויקט עודכן בהצלחה');
			notifier.success('הפרויקט עודכן בהצלחה', {
				// position: 'bottom-right',
				timeout: 3000
			});
			form_data = JSON.parse(JSON.stringify(p_data));
			original_data = JSON.parse(JSON.stringify(p_data));

			goto(`/done-projects/`);
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
	<EditProject bind:form_data on_update_function={update_project} {original_data} />
{/if}

<style lang="scss">
</style>
