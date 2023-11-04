<script>
	import { closeModal } from 'svelte-modals';
	import { network_approve_rejected_project } from '$lib/network.js';
	import { notifier } from '@beyonk/svelte-notifications';
	import { goto } from '$app/navigation';

	export let isOpen;
	export let title = 'אישור פרויקט דחוי';
	export let project_name;
	export let project_id;
	export let message = 'האם ברצונך לאשר את הפרויקט ' + project_name;

	function handleApproveClick() {
		// openModal(ModalApprove, { awaiting_project_id: form_data.id });
		network_approve_rejected_project(project_id).then((res) => {
			if (res.status == 200) {
				notifier.success('הפרויקט אושר בהצלחה', {
					// position: 'bottom-right',
					timeout: 3000
				});
				closeModal();
				goto('/waiting-approval');
			} else {
				notifier.danger('אירעה שגיאה בעת אישור הפרויקט', {
					// position: 'bottom-right',
					timeout: 3000
				});
			}
		});
	}
</script>

{#if isOpen}
	<div role="dialog" class="modal">
		<div class="contents">
			<div>
				<h2>{title}</h2>
				<p>{message}</p>
				<div class="actions">
					<button class="btn btn-success" on:click={handleApproveClick}>אשר</button>
					<button class="btn btn-secondary" on:click={closeModal}>חזור</button>
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
		justify-content: space-around;
	}
</style>
