<script>
	import TableViewPage from '../../comonents/list-view/TableViewPage.svelte';
	import { API_REJECTED_PROJECT, API_REJECTED_PROJECT_DESCRIPTION } from '$lib/consts';
	import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  onMount(async()=>{
	let token=localStorage.getItem("token")
	if(!token){
		goto("/login")
	}
  })
</script>

<!-- TODOO -->
