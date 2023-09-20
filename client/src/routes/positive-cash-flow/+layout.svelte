<!-- 3 links -->
<script>
	import { page } from '$app/stores';
	let links = [
		// {
		// 	name: 'לפי לקוח',
		// 	url: `/positive-cash-flow/client`
		// },
		{
			name: 'לפי פרויקט',
			url: `/positive-cash-flow/project`
		},
		{
			name: 'לפי חשבונית',
			url: `/positive-cash-flow/invoice`
		}
	];
</script>

<!-- client, project, invoice -->
<div class="container">
	<div class="row">
		<div class="col-12">
			<div class="btn-group" role="group" aria-label="Basic example">
				{#each links as link}
					<a href={link.url} class="btn btn-primary" class:active={$page.url.pathname === link.url}
						>{link.name}</a
					>
				{/each}
			</div>
		</div>
	</div>
</div>
<slot />
