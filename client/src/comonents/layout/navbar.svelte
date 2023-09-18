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
			name: 'הגדרות',
			isDropdown: true,
			dropdownOptions: [
				{
					name: 'סטטוסים',
					url: '/status'
				},
				{
					name: 'הערות',
					url: '/comments'
				}
			]
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
	<!-- 	<div class="collapse navbar-collapse" id="navbarNav">
			<ul class="navbar-nav">
				{#each info as item}
					<li class="nav-item" class:active={$page.url.pathname.includes(item.url)}>
						<a class="nav-link" href={item.url}>{item.name}</a>
					</li>
				{/each}
			</ul>
		</div> -->
			<div class="collapse navbar-collapse" id="navbarNav">
			<ul class="navbar-nav">
				{#each info as item}
					{#if item.isDropdown} <!-- Check if it's a dropdown item -->
						<li class="nav-item dropdown">
							<a
								class="nav-link dropdown-toggle"
								href="#"
								id="navbarDropdown"
								role="button"
								data-bs-toggle="dropdown"
								aria-expanded="false"
							>
								{item.name}
							</a>
							<ul class="dropdown-menu" aria-labelledby="navbarDropdown">
								{#each item.dropdownOptions as dropdownItem}
									<li>
										<a class="dropdown-item" href={dropdownItem.url}>
											{dropdownItem.name}
										</a>
									</li>
								{/each}
							</ul>
						</li>
					{:else}
						<li class="nav-item" class:active={$page.url.pathname.includes(item.url)}>
							<a class="nav-link" href={item.url}>{item.name}</a>
						</li>
					{/if}
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
