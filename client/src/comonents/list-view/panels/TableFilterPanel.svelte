<script>
	import DateFilter from './../filter/DateFilter.svelte';
	import MultiSelectFilter from './../filter/MultiSelectFilter.svelte';

	import TextFilter from './../filter/TextFilter.svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { PAGE_SIZE_QUERY_PARAM, PAGINATION_QUERY_PARAM } from '$lib/consts.js';
	let filter_elements = {};
	let selected_page_size_value = undefined;
	export let description;
	let curr_fullpage_url = undefined;
	$: {
		if (description && description['api-description']) {
			curr_fullpage_url = $page.url.toString();
		}
	}
	onMount(() => {
		// fill_filters_based_on_query_params();
	});
	$: {
		filter_elements;
		fill_filters_based_on_query_params();
		console.log('url_key', curr_fullpage_url);
	}

	function fill_filters_based_on_query_params() {
		for (const [key, value] of Object.entries(filter_elements)) {
			value.set_from_url(curr_fullpage_url);
		}

		// set the page size
		if (curr_fullpage_url) {
			let split_url = curr_fullpage_url.split('?');
			if (split_url.length > 1) {
				const url_params = new URLSearchParams(split_url[1]);
				selected_page_size_value = url_params.get(PAGE_SIZE_QUERY_PARAM);
				if (selected_page_size_value) {
					description['api-description'].pagination = selected_page_size_value;
				}
			}
		}
	}
	// {"api-description":{"extra":{"client_options":[{"value":1,"label":"client1"},{"value":2,"label":"client2"},{"value":3,"label":"asd"}]},"filters":{"name":{"type":"text","name":"שם","slug":"name"},"client":{"type":"select","options":"client_options","name":"לקוח","slug":"client"},"created_at":{"type":"date","name":"נוצר בתאריך","slug":"created_at"},"updated_at":{"type":"date","name":"עודכן בתאריך","slug":"updated_at"}},"search":{"name":{"type":"text"},"client":{"type":"select","options":"client_options"}},"ordering":{"name":{"type":"text"},"client":{"type":"select","options":"client_options"},"created_at":{"type":"date"},"updated_at":{"type":"date"}},"pagination":{"type":"None"},"fields":{"name":{"type":"text"},"client":{"type":"select","options":"client_options"},"created_at":{"type":"date"},"updated_at":{"type":"date"}},"actions":{"type":"None"},"permissions":{"type":"None"}}}

	function preform_filter() {
		const url_params = new URLSearchParams(window.location.search);
		// let query_params = '';
		// iterate over filter_elements
		for (const [key, value] of Object.entries(filter_elements)) {
			// get query param from each filter
			let query_param = value.get_query_param();
			// query_param = [ { name: 'name', value: 'value' }]
			// if query param is not empty, add it to query_params
			if (query_param.length > 0) {
				for (const param of query_param) {
					url_params.set(param.name, param.value);
				}
			}
		}

		// add the page_size to the url
		url_params.set(PAGE_SIZE_QUERY_PARAM, description['api-description'].pagination);

		// set the page to 1
		url_params.set(PAGINATION_QUERY_PARAM, 1);

		location.href = `${$page.url.pathname}?${url_params.toString()}`;
	}

	function reset_filter() {
		// iterate over filter_elements
		for (const [key, element] of Object.entries(filter_elements)) {
			// reset each filter
			element.reset_filter();
		}
	}
</script>

<!-- bootstrap show aside with the filters -->
<aside class="col-3">
	<div class="card">
		<div class="card-header">
			<h4 class="card-title">מסננים</h4>
		</div>
		<div class="card-body aside-filters">
			{#if description}
				<!-- iterate over description['api-description'].filters keys, 
                if type is text, show input
                if type is select, show select
                if type is date, start date and end date
            -->
				{#each Object.keys(description['api-description'].filters) as filter_key}
					{@const filter = description['api-description'].filters[filter_key]}
					{#if filter.type == 'text'}
						<TextFilter
							title={filter.name}
							slug={filter.slug}
							bind:value={description['api-description'].filters[filter_key].entered_value}
							bind:this={filter_elements[filter_key]}
						/>
					{:else if filter.type == 'multi-select'}
						<MultiSelectFilter
							title={filter.name}
							slug={filter.slug}
							options={description['api-description'].extra[filter.options]}
							bind:value={description['api-description'].filters[filter_key].entered_value}
							bind:this={filter_elements[filter_key]}
						/>
					{:else if filter.type == 'date'}
						<DateFilter
							title={filter.name}
							slug={filter.slug}
							bind:value={description['api-description'].filters[filter_key].entered_value}
							bind:this={filter_elements[filter_key]}
						/>
					{/if}
				{/each}

				<!-- pagination options: 20, 50, 100, 99999 -->
				<div class="form-group">
					<label for="pagination">הצג בדף</label>
					<select
						class="form-control"
						id="pagination"
						bind:value={description['api-description'].pagination}
					>
						<option value="50">50</option>
						<option value="150">150</option>
						<option value="99999">הכל</option>
					</select>
				</div>

				<div class="form-group">
					<br />
					<button type="button" class="btn btn-primary btn-block" on:click={preform_filter}
						>החל</button
					>
					<button type="button" class="btn btn-secondary btn-block" on:click={reset_filter}>
						אפס
					</button>
				</div>
			{:else}
				<!-- <div class="spinner-border" role="status">
					<span class="sr-only" />
				</div> -->
			{/if}
		</div>
	</div>
</aside>

<style lang="scss">
	.aside-filters {
	}
	.card {
		margin-bottom: 1rem;
		.card-body {
			padding: 0.5rem;
			:global(.form-group) {
				margin-bottom: 0.7rem;
			}
		}
	}
</style>
