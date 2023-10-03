<script>
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import { network_update_awaiting_project } from '$lib/network.js';
	import EditAwaitingProject from '../../../comonents/EditAwaitingProject.svelte';
	// export let data;
	import { beforeNavigate } from '$app/navigation';
	import { onMount } from 'svelte';
	import { API_AWAITING_PROJECTS } from '$lib/consts';
	import { notifier } from '@beyonk/svelte-notifications';

	let form_data = undefined;
	let original_data = undefined;

	onMount(async () => {
		let url = `${API_AWAITING_PROJECTS}${$page.params.id}/`;
		console.log('fetching awaiting project data from server', url);
		const res = await fetch(url);
		const data = await res.json();
		original_data = JSON.parse(JSON.stringify(data));
		form_data = JSON.parse(JSON.stringify(data));
	});

	function project_total_changed(new_data) {
		let ret = original_data.api_data.total != form_data.api_data.total;
		return ret;
	}

	async function update_project(project_id, p_data, ret_url) {
		debugger;
		if (project_total_changed()) {
			let res = confirm('הסכום השתנה, האם ברצונך להפיק הצעת מחיר חדשה ללקוח?');
			if (res) {
				p_data.submit_for_approval = true;
			}
		}
		const res = await network_update_awaiting_project(project_id, p_data);
		console.log('res: ', res);
		if (res.status == 200) {
			notifier.success('הפרויקט עודכן בהצלחה', {
				// position: 'bottom-right',
				timeout: 3000
			});
			form_data = JSON.parse(JSON.stringify(p_data));
			original_data = JSON.parse(JSON.stringify(p_data));
			debugger;
			if (ret_url && ret_url != $page.url.pathname) {
				goto(ret_url);
			}
		}
		return res;
	}

	// beforeNavigate we check if form_data is diffrent from data.project_data (the original data)
	// if it is diffrent we ask the user if he wants to save the changes
	// if he does we call update_project
	// if he doesn't we just navigate to the new page
	beforeNavigate(async ({ to, cancel }) => {
		if (JSON.stringify(form_data) != JSON.stringify(original_data)) {
			if (confirm('האם ברצונך לשמור את השינויים לפי יציאה מהעמוד?')) {
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

<div class="row" style="display: flex;flex-direction:row;">
	<div class="col">
		form_data
		<pre>
			{JSON.stringify(form_data?.api_data?.subtotal)}
		</pre>
	</div>
	<div class="col">
		original_data
		<pre>
			{JSON.stringify(original_data?.api_data?.subtotal)}
		</pre>
	</div>
</div>
{#if form_data}
	<EditAwaitingProject bind:form_data on_update_function={update_project} />
{/if}

<style lang="scss">
</style>
