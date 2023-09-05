<script>
	import { onMount } from 'svelte';

	// items = [{id: 1, label: 'item1', selected: false},...]
	export let items = [];

	export let activeTabId = 1;
	// const handleClick = (tabValue) => () => (activeTabId = tabValue);
	onMount(() => {
		// get the tab id from the url hash
		const hash = window.location.hash;
		if (hash) {
			const tabId = parseInt(hash.replace('#', ''));
			if (tabId) {
				activeTabId = tabId;
			}
		}
	});
	function handleClick(tabValue) {
		return function () {
			activeTabId = tabValue;
			// add to url hash the tab id
			window.location.hash = tabValue;
		};
	}
</script>

<ul>
	{#each items as item}
		<li on:click={handleClick(item.id)} class={activeTabId === item.id ? 'active' : ''}>
			<span>{item.label}</span>
		</li>
	{/each}
</ul>

<style>
	ul {
		display: flex;
		flex-wrap: wrap;
		padding-left: 0;
		margin-bottom: 0;
		list-style: none;
		border-bottom: 1px solid #dee2e6;
	}
	li {
		margin-bottom: -1px;
	}

	span {
		border: 1px solid transparent;
		border-top-left-radius: 0.25rem;
		border-top-right-radius: 0.25rem;
		display: block;
		padding: 0.5rem 1rem;
		cursor: pointer;
	}

	span:hover {
		border-color: #e9ecef #e9ecef #dee2e6;
	}

	li.active > span {
		color: #495057;
		background-color: #fff;
		border-color: #dee2e6 #dee2e6 #fff;
	}
</style>
