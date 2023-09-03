<!-- text input to acceput the order number, without if, can not click ok and continue -->

<script>
	import { onMount } from 'svelte';
	import { closeModal } from 'svelte-modals';
	import { network_approve_awaiting_project } from '$lib/network.js';
	export let awaiting_project_id;
	let inputElement;
	let order_num = '';
	// provided by <Modals />
	export let isOpen;
	$: {
		if (isOpen && inputElement) {
			inputElement.focus();
		}
	}
	function submit() {
		network_approve_awaiting_project(awaiting_project_id, order_num).then((res) => {
			console.log('res: ', res);
			if (res.status == 200) {
				alert('הפרויקט אושר בהצלחה');
			}
		});
		closeModal();
	}
</script>

{#if isOpen}
	<div role="dialog" class="modal">
		<div class="contents">
			<div>
				<h2>הזן מספר הזמנה</h2>
				<p>
					<input
						type="text"
						class="form-control"
						id="order_num"
						bind:this={inputElement}
						bind:value={order_num}
						on:keypress={(e) => {
							if (e.key === 'Enter' && order_num) {
								submit();
							}
						}}
					/>
				</p>
				<div class="actions">
					<button on:click={submit} disabled={!order_num} class="btn btn-primary">שלח</button>
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
