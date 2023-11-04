<script>
	import { onMount } from 'svelte';
	import { closeModal } from 'svelte-modals';
	import { MultiSelect } from 'svelte-multiselect';
	import { notifier } from '@beyonk/svelte-notifications';

	import { fly } from 'svelte/transition';
	import { fade } from 'svelte/transition';
	import {
		network_get_all_reject_reasons_select,
		network_reject_awaiting_project
	} from '$lib/network.js';

	// provided by <Modals />
	export let isOpen;
	export let awaiting_project_id;
	let value;
	let options;
	onMount(() => {
		network_get_all_reject_reasons_select().then((res) => {
			console.log('res: ', res);
			if (res.status == 200) {
				res.json().then((data) => {
					options = data;
				});
			}
		});
	});

	function submit() {
		console.log('submit');
		console.log('value: ', value);
		let error = undefined;
		network_reject_awaiting_project(awaiting_project_id, value).then((res) => {
			console.log('res: ', res);
			if (res.status == 200) {
				notifier.success('הפרויקט נדחה בהצלחה');
			} else {
			}
		});

		closeModal();
	}
</script>

{#if isOpen}
	<div role="dialog" class="modal">
		<div class="contents">
			<div>
				<h2>סיבת הדחייה</h2>
				<p>
					{#if options}
						<MultiSelect
							bind:value
							{options}
							maxSelect={1}
							allowUserOptions={true}
							createOptionMsg="הוסף סיבה חדשה"
						/>
					{/if}
				</p>
				<div class="actions">
					<button on:click={submit} class="btn btn-primary" disabled={!value}>שלח</button>
				</div>
			</div>
		</div>
	</div>
{/if}

<style>
	.modal {
		position: fixed;
		top: 0;
		bottom: 0;
		right: 0;
		left: 0;
		display: flex;
		justify-content: center;
		align-items: center;

		/* allow click-through to backdrop */
		pointer-events: none;
	}

	.contents {
		min-width: 240px;
		border-radius: 6px;
		padding: 16px;
		background: white;
		display: flex;
		flex-direction: column;
		justify-content: space-between;
		pointer-events: auto;
	}

	h2 {
		text-align: center;
		font-size: 24px;
	}

	p {
		text-align: center;
		margin-top: 16px;
	}

	.actions {
		margin-top: 32px;
		display: flex;
		justify-content: flex-end;
	}
</style>
