<script>
	import '../app.scss';
	import { page } from '$app/stores';
	import Navbar from '../comonents/layout/navbar.svelte';
	import Breadcrumb from '../comonents/Breadcrumb.svelte';
	import { Modals, closeModal } from 'svelte-modals';
	import { fade } from 'svelte/transition';

	// $page.data.nav_data
</script>

<Navbar data={$page.data.nav_data} />
<Breadcrumb />

<Modals>
	<div slot="backdrop" transition:fade={{ duration: 200 }} class="backdrop" on:click={closeModal} />
</Modals>

<slot />

<style>
	.backdrop {
		position: fixed;
		top: 0;
		bottom: 0;
		right: 0;
		left: 0;
		background: rgba(0, 0, 0, 0.5);
		z-index: 100;
	}
</style>
