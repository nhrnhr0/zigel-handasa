<!-- redirect to .../client -->
<script>
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	onMount(() => {
		debugger;
		if ($page.url.pathname === '/positive-cash-flow') {
			goto('/positive-cash-flow/invoice');
		}
	});
</script>

het
