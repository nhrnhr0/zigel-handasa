<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
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
			name: 'דוח תזרים חיובי',
			url: '/positive-cash-flow'
		},
		{
			name: 'פרויקטים גמורים',
			url: '/done-projects'
		}
	];
	// let istoken=false;
	// onMount(async()=>{
	// 	const token=localStorage.getItem("token")
	// 	if(token){
	// 		istoken=true
	// 	}
	// })
	function logOut(){
		localStorage.removeItem("token")
		goto("/login")

	}
	function handleKeyPress(event){
		if(event.key==='Enter'){
			logOut()
		}
	}
</script>
{#if $page.url.pathname !== '/login'}
<nav class="navbar navbar-expand-lg navbar-light bg-light" >
	<div class="container-fluid">
		<a class="navbar-brand" href="/">PMS</a>
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
			<div class=navbaar-nav>
				<span on:click={logOut} class="nav-item" id="logout-span">
					<span class="nav-link" style="cursor: pointer;" id="logout">התנתק</span>
				</span>
				</div>
		</div>
	</div>
</nav>
{/if}
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
	#logout{
		min-height: 40px;
		display: flex;
		align-items: center;
		justify-content: center;
		padding-left: 5px;
		padding-right: 5px;
	}
	#logout:hover{
		color: white;
		background-color: #f44336;
		
	}
	#navbarNav{
		display: flex;
		justify-content: space-between;
	}
</style>
