<script>
	import { fly } from 'svelte/transition';
	import { createEventDispatcher } from 'svelte';
	export let isOpen = false; // To track whether the action list is open or closed
	// Array of actions
	export let actions = ['Action 1', 'Action 2', 'Action 3'];

	// event dispatcher
	const dispatch = createEventDispatcher();

	function action_clicked(e) {
		// console.log(e.target.innerText);
		dispatch('action_clicked', e.target.innerText);
		isOpen = false;
	}
	// Function to toggle the visibility of the action list
	export function toggleActions() {
		isOpen = !isOpen;
	}
</script>

<!-- The main component -->
<div class="action-dropdown">
	<slot name="button">
		<button
			on:click={toggleActions}
			class="btn rounded-0 action-btn"
			type="button"
			class:active={isOpen}
		>
			<div class="my-svg">
				<svg
					xmlns="http://www.w3.org/2000/svg"
					width="24"
					height="24"
					fill="currentColor"
					class="bi bi-plus-circle"
					viewBox="0 0 16 16"
				>
					<path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z" />
					<path
						d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z"
					/>
				</svg>
			</div>
		</button>
	</slot>
	{#if isOpen}
		<slot name="actions">
			<ul in:fly={{ y: 10, duration: 300 }}>
				{#each actions as action (action)}
					<li class="action" on:click={action_clicked}>{action}</li>
				{/each}
			</ul>
		</slot>
	{/if}
</div>

<style lang="scss">
	/* Basic CSS for styling the component */
	.action-dropdown {
		position: relative;
	}
	.action-btn {
		padding: 0px;
		margin: 0px;
		border: none;
		background-color: transparent;
		outline: none;
	}

	ul {
		list-style: none;
		padding: 0;
		margin: 0;
		position: absolute;
		background-color: #fff;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
		border: 1px solid #ccc;
		z-index: 1;

		li {
			padding: 10px;
			width: 100%;
			min-width: 160px;

			cursor: pointer;
			&:hover {
				background-color: #f1f1f1;
			}
		}
	}
</style>
