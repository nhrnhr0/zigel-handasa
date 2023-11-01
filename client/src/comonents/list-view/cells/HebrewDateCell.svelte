<script>
	export let data;
</script>

<td>
	{#if data}
		{new Date(data).toLocaleString('he-IL', {
			timeZone: 'Asia/Jerusalem',
			dateStyle: 'short'
		})}
	{/if}
</td>
