<script>
	import { page } from '$app/stores';
	// export let data;
	let info = [
		{
			name: 'ממתינים לאישור',
			url: '/waiting-approval'
		},
		{
			name: 'פרויקטים',
			url: '/projects'
		},
		{
			name: 'פרויקטים דחויים',
			url: '/rejected-project'
		},
		{
			name: 'כספים',
			url: '/accounting'
		},
		{
			name:'הוסף קבצים',
			url:'/upload-fiels'
		}
	];
</script>

<nav class="navbar navbar-expand-lg navbar-light bg-light">
	<div class="container-fluid">
		<a class="navbar-brand" href="#">PMS</a>
		<button
			class="navbar-toggler"
			type="button"
			data-bs-toggle="collapse"
			data-bs-target="#navbarNav"
			aria-controls="navbarNav"
			aria-expanded="false"
			aria-label="Toggle navigation"
		>
			<span class="navbar-toggler-icon" />
		</button>
		<div class="collapse navbar-collapse" id="navbarNav">
			<ul class="navbar-nav">
				{#each info as item}
					<li class="nav-item" class:active={$page.url.pathname.includes(item.url)}>
						<a class="nav-link" href={item.url}>{item.name}</a>
					</li>
				{/each}
			</ul>
		</div>
	</div>
</nav>

<style lang="scss">
	.navbar {
		.nav-item {
			&.active {
				a {
					color: #fff;
					background-color: #0d6efd;
					border-color: #0d6efd;
				}
			}
		}
	}
</style>
