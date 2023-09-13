<script>
	import { onMount } from 'svelte';
	import { PAGINATION_QUERY_PARAM, PAGE_SIZE_QUERY_PARAM } from '$lib/consts.js';
	export let api_data;

	// {
	// "count": 1004,
	// "next": "http://127.0.0.1:8000/awaiting-projects/?page=2",
	// "previous": null,
	// "results": [....
	// we display links for the closest 2 pages to the current page and the first and last page
	let pagination_links = [];
	let current_page = -1;
	let page_size = -1;
	let count = 0;
	let last_page_index = 0;
	onMount(() => {
		const url_params = new URLSearchParams(window.location.search);
		current_page = parseInt(url_params.get(PAGINATION_QUERY_PARAM) || '1');
		if (current_page < 1) {
			current_page = 1;
		}

		page_size = parseInt(url_params.get(PAGE_SIZE_QUERY_PARAM) || '50');
		// get the count of the results
		// count = api_data.count;
		// // get the last page
		// last_page_index = Math.ceil(count / page_size);
		// get the first page
	});

	$: {
		count = api_data?.count || 0;
		last_page_index = Math.ceil(count / page_size);
	}

	function preform_navigation(e) {
		console.log('preform_navigation', e.target.innerText);
		let new_page = current_page;
		if (e.target.innerText === 'התחלה') {
			new_page = 1;
		} else if (e.target.innerText === 'הקודם') {
			new_page = current_page - 1;
		} else if (e.target.innerText === 'הבא') {
			new_page = current_page + 1;
		} else if (e.target.innerText === 'סוף') {
			new_page = last_page_index;
		} else {
			new_page = parseInt(e.target.innerText);
		}
		if (new_page < 1) {
			new_page = 1;
		}
		if (new_page > last_page_index) {
			new_page = last_page_index;
		}
		console.log('new_page', new_page);
		const url_params = new URLSearchParams(window.location.search);
		url_params.set(PAGINATION_QUERY_PARAM, new_page);
		window.location.href = `${window.location.pathname}?${url_params.toString()}`;
	}
</script>

<nav aria-label="Page navigation example" class="pagination-nav">
	<!-- results text:
        דף 1 מתוך 10
        100 תוצאות
    -->
	<div class="results-text">
		<span class="page-number">דף {current_page} מתוך {last_page_index}</span>

		<span class="results-count">{count} תוצאות</span>
	</div>
	<ul class="pagination">
		<li class="page-item" class:disabled={current_page == 1}>
			<a class="page-link" on:click={preform_navigation} href="#">התחלה</a>
		</li>
		<li class="page-item" class:disabled={current_page == 1}>
			<a class="page-link" on:click={preform_navigation} href="#">הקודם</a>
		</li>
		{#if current_page > 3}
			<li class="page-item disabled">
				<a class="page-link" href="#">...</a>
			</li>
		{/if}

		{#if current_page > 2}
			<li class="page-item">
				<a class="page-link" on:click={preform_navigation} href="#">{current_page - 2}</a>
			</li>
		{/if}
		{#if current_page > 1}
			<li class="page-item">
				<a class="page-link" on:click={preform_navigation} href="#">{current_page - 1}</a>
			</li>
		{/if}

		<li class="page-item active">
			<a class="page-link" on:click={preform_navigation} href="#">{current_page} </a>
		</li>

		{#if current_page <= last_page_index - 1}
			<li class="page-item">
				<a class="page-link" on:click={preform_navigation} href="#">{current_page + 1}</a>
			</li>
		{/if}
		{#if current_page <= last_page_index - 2}
			<li class="page-item">
				<a class="page-link" on:click={preform_navigation} href="#">{current_page + 2}</a>
			</li>
		{/if}
		{#if current_page <= last_page_index - 3}
			<li class="page-item">
				<a class="page-link" on:click={preform_navigation} href="#">{current_page + 3}</a>
			</li>
		{/if}
		{#if current_page <= last_page_index - 4}
			<li class="page-item disabled">
				<a class="page-link" href="#">...</a>
			</li>
		{/if}

		<li class="page-item" class:disabled={current_page == last_page_index}>
			<a class="page-link" on:click={preform_navigation} href="#">הבא</a>
		</li>

		<li class="page-item" class:disabled={current_page == last_page_index}>
			<a class="page-link" on:click={preform_navigation} href="#">סוף</a>
		</li>
	</ul>
</nav>

<style lang="scss">
	.pagination-nav {
		position: relative;
		.pagination {
			justify-content: center;
		}
	}
	.results-text {
		position: absolute;
		margin-left: 1rem;
		margin-right: 1rem;
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 1rem;
		.page-number {
			font-size: 1.2rem;
			padding: 0.5rem;
		}
		.results-count {
			font-size: 1.2rem;
			padding: 0.5rem;
		}
	}
</style>
