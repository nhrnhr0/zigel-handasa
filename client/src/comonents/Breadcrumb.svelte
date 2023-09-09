<script lang="ts">
	const PAGE_LABELS = {
		'waiting-approval': 'פרויקטים ממתינים לאישור',
		projects: 'פרויקטים',
		'rejected-project': 'פרויקטים דחויים',
		accounting: 'כספים'
	};
	import { page } from '$app/stores';

	let crumbs: Array<{ label: string; href: string }> = [];

	$: {
		// Remove zero-length tokens.
		const tokens = $page.url.pathname.split('/').filter((t) => t !== '');
		debugger;

		debugger;
		// Create { label, href } pairs for each token.
		let tokenPath = '';
		crumbs = tokens.map((t) => {
			tokenPath += '/' + t;
			// get the +page of the tokenPath

			return {
				label: PAGE_LABELS[t] || t,
				href: tokenPath
			};
		});

		// Add a way to get home too.
		crumbs.unshift({ label: 'דף בית', href: '/' });
	}
</script>

<div class="breadcrumb">
	{#each crumbs as c, i}
		{#if i == crumbs.length - 1}
			<span class="label">
				{c.label}
			</span>
		{:else}
			<a href={c.href}>{c.label}</a> &gt;&nbsp;
		{/if}
	{/each}
</div>

<style>
	.breadcrumb {
		margin: 0 1.5rem;
		padding: 1rem 2rem;
	}

	.breadcrumb a {
		display: inline-block;
		color: blue;
		padding: 0 0.5rem;
		text-decoration: none;
	}

	.breadcrumb .label {
		padding-left: 0.5rem;
		color: black;
	}
</style>
