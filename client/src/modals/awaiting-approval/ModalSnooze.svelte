<!-- text input to acceput the order number, without if, can not click ok and continue -->

<script>
	import { onMount } from 'svelte';
	import { closeModal } from 'svelte-modals';
	import { network_snooze_awaiting_project } from '$lib/network.js';
	export let awaiting_project_id;
	let selectElement;
	let inputElement;
	let selectValue = '7';
	let inputValue = '';
	// provided by <Modals />
	export let isOpen;
	$: {
		if (isOpen && selectElement) {
			selectElement.focus();
		}
	}
	function submit() {
		let val = selectValue;
		if (selectValue == 'other') {
			val = inputValue;
		}
		console.log('val: ', val);
		network_snooze_awaiting_project(awaiting_project_id, val).then((res) => {
			console.log('res: ', res);
			if (res.status == 200) {
				alert('הפרויקט דחה בהצלחה');
			}
		});
		closeModal();
	}
</script>

{#if isOpen}
	<div role="dialog" class="modal">
		<div class="contents">
			<div>
				<h2>למתי לדחות את ההתראה?</h2>
				<div>
					<!-- שבוע, שבועיים, חודש, אחר (הכנס מספר) -->
					<select class="form-control" bind:value={selectValue} bind:this={selectElement}>
						<option value="7">שבוע</option>
						<option value="14">שבועיים</option>
						<option value="30">חודש</option>
						<option value="other">אחר</option>
					</select>
					{#if selectValue == 'other'}
						<br />
						<label for="custom" class="">הכנס מספר ימים לדחייה</label>
						<input
							type="number"
							class="form-control"
							id="custom"
							bind:this={inputElement}
							bind:value={inputValue}
							on:keypress={(e) => {
								if (e.key === 'Enter' && inputValue) {
									submit();
								}
							}}
						/>
					{/if}
				</div>
				<div class="actions">
					<button
						on:click={submit}
						class="btn btn-primary"
						disabled={!selectValue || (selectValue == 'other' && !inputValue)}>שמור</button
					>
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
