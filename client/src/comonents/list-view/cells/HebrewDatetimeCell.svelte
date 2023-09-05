<script>
	export let data;
</script>

{#if data}
	{new Date(data).toLocaleString('he-IL', {
		timeZone: 'Asia/Jerusalem'
	})}
{/if}
