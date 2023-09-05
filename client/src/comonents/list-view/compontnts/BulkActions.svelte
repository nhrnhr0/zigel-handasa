<script>
	import { fly } from 'svelte/transition';
	export let actions = [];
	export let selected_data = [];
	export let clear_select;
</script>

{#if actions && actions.length > 0}
	<div class="bulk-actions" transition:fly={{ y: 100, duration: 200 }}>
		<label for="bulk-actions">בחר פעולה ({selected_data.length} פריטים)</label>
		<div class="form-group">
			<select class="form-control" style="width: 200px; margin-right: 20px;">
				{#each actions as action}
					<option value={action.label}>{action.label}</option>
				{/each}
			</select>
			<button class="btn btn-primary">בצע</button>
		</div>

		<div class="exit">
			<button class="btn exit-btn" on:click={clear_select}> X </button>
		</div>
	</div>
{/if}

<style lang="scss">
	.bulk-actions {
		display: flex;
		width: 600px;
		height: 120px;
		padding: 15px 35px;
		border-radius: 12px;
		background: #fff;
		position: fixed;
		bottom: 100px;
		left: 50%;
		transform: translateX(-50%);
		box-shadow: -1px 1px 10px rgba(0, 0, 0, 0.1);
		z-index: 100;
		display: flex;
		flex-direction: column;
		.form-group {
			label {
				margin-left: 20px;
			}
			margin: 1rem;
			display: flex;
			align-items: center;
			justify-content: center;
		}
		.exit-btn {
			position: absolute;
			top: 0;
			left: 0;
			// margin: 10px;
			padding: 5px 10px;
			// border-radius: 50%;
			border: none;
			// background: #fff;
			// box-shadow: -1px 1px 10px rgba(0, 0, 0, 0.1);

			cursor: pointer;
			&:hover {
				background: #eee;
			}
		}
	}
</style>
