<script>
	import { scale } from 'svelte/transition';
	let mouse_x = 0;
	let mouse_y = 0;
	export let is_show = false;
	export let active = true;
</script>

<!-- slot title and content -->

<!-- show title -->
<button
	class="btn title"
	on:click={(event) => {
		if (active) {
			mouse_x = event.clientX;
			// mouse_y = event.clientY + 35;
			// mouse_y = end of the button
			mouse_y = event.target.offsetHeight + event.target.top;
			is_show = !is_show;
		}
	}}
>
	<slot />
</button>
{#if is_show}
	<div class="content" transition:scale style="left: {mouse_x}px; top: {mouse_y}px;">
		<div class="exit">
			<button class="btn" on:click={() => (is_show = false)}>X</button>
		</div>
		<div class="wraper">
			<slot name="content" />
		</div>
	</div>
{/if}

<style lang="scss">
	.title {
		cursor: pointer;
	}

	.content {
		// position: relative;
		border: 1px solid #ccc;
		border-radius: 5px;
		position: absolute;
		background-color: white;
		z-index: 1;
		transform: translate(-50%, 0);
		.exit {
			width: 100%;
			text-align: right;
			.btn {
				padding: 3px;
				margin: 0px;
			}
		}

		.wraper {
			padding: 10px;
		}
	}
</style>
