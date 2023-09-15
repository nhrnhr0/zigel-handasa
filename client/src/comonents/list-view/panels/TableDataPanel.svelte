<script>
	import { scale } from 'svelte/transition';
	import { page } from '$app/stores';
	import { createEventDispatcher, onMount } from 'svelte';
	import RawCell from '../cells/RawCell.svelte';
	import PaginationResult from '../compontnts/PaginationResult.svelte';
	import { SEARCH_QUERY_PARAM, ORDERING_QUERY_PARAM } from '$lib/consts.js';
	import HebrewDateCell from '../cells/HebrewDateCell.svelte';
	import HebrewDateTimeCell from '../cells/HebrewDatetimeCell.svelte';
	import TestCustomCell from '../cells/custom/TestCustomCell.svelte';
	import AwaitingProjectsActionCell from '../cells/custom/AwaitingProjectsActionCell.svelte';
	import ProjectsActionCell from '../cells/custom/ProjectsActionCell.svelte';
	import BulkActions from '../compontnts/BulkActions.svelte';
	import CurrencyCell from '../cells/currencyCell.svelte';
	import AwaitingProjectsAlertDateCell from '../cells/custom/AwaitingProjectsAlertDateCell.svelte';
	import ProjectsProgressCell from '../cells/custom/ProjectsProgressCell.svelte';
	export let description;
	export let api_data;
	export let allow_select;
	let search_term = '';
	export let selected_ids = {};
	export let select_all = false;
	export let actions;
	export let selected_data;
	export let pagination = true;
	export let show_search_bar = true;
	export let custom_height = undefined;
	export let on_select_change = undefined;
	export let expendable = false;
	let expended_rows = {};

	function select_all_rows(e) {
		if (e.target.checked) {
			// selected_rows = api_data.results;
			let list = api_data.results.map((r) => r.id);
			selected_ids = {};
			for (const id of list) {
				selected_ids[id] = true;
			}
		} else {
			selected_ids = {};
		}
		select_all = e.target.checked;
		update_selected_data();
		if (on_select_change) {
			on_select_change(selected_ids, selected_data);
		}
	}

	function check_if_all_selected() {
		let all_selected_ids_are_true = true;
		for (const [key, value] of Object.entries(selected_ids)) {
			if (value === false) {
				all_selected_ids_are_true = false;
			}
		}
		select_all =
			api_data.results.length === Object.values(selected_ids).length && all_selected_ids_are_true;
	}

	function update_selected_data() {
		let selected_ids_array = Object.entries(selected_ids)
			.filter((e) => e[1] === true)
			.map((e) => e[0]);
		selected_data = api_data.results.filter((row) =>
			selected_ids_array.includes(row.id.toString())
		);
	}
	function select_row(e) {
		if (selected_ids[e.id]) {
			delete selected_ids[e.id];
		} else {
			selected_ids[e.id] = true;
		}
		check_if_all_selected();
		update_selected_data();

		if (on_select_change) {
			on_select_change(selected_ids, selected_data);
		}
	}
	function clear_select() {
		selected_ids = {};
		select_all = false;
		update_selected_data();
		if (on_select_change) {
			on_select_change(selected_ids, selected_data);
		}
	}

	let table_height_px = custom_height || `calc(100vh - 300px)`;

	onMount(() => {
		// check if search term is in the url
		const url_params = new URLSearchParams(window.location.search);
		search_term = url_params.get(SEARCH_QUERY_PARAM) || '';
	});

	$: {
		if (description && description['api-description']) {
			init_after_description_set();
		}
	}
	function init_after_description_set() {
		const url_params = new URLSearchParams(window.location.search);

		// check if there is a sort param in the url (ordering)
		// http://127.0.0.1:8000/awaiting-projects/?client__in=1%2C2&ordering=client__name,-name
		const ordering = url_params.get(ORDERING_QUERY_PARAM) || '';
		console.log('ordering', ordering);
		// add to each field if it is sorted and how
		// description['api-description'].fields[field_key].sorted = 'asc' | 'desc' | undefined
		for (const [key, value] of Object.entries(description['api-description'].fields)) {
			value.sorted = undefined;
		}
		// split by comma
		const ordering_fields = ordering.split(',');
		// remove empty strings

		// iterate over each field
		let i = 0;
		let field_key = '';
		for (const field of ordering_fields) {
			// if field starts with - it is sorted desc
			if (field === '') continue;
			if (field.startsWith('-')) {
				// remove the -
				field_key = field.slice(1);
				// add sorted desc to the field
				description['api-description'].fields[field_key].sorted = 'desc';
			} else {
				// add sorted asc to the field
				field_key = field;
				description['api-description'].fields[field_key].sorted = 'asc';
			}
			description['api-description'].fields[field_key].sort_order = i;
			i++;
		}
	}
	function search_on_enter(e) {
		if (e.key === 'Enter') {
			preform_search();
		}
	}
	function preform_search() {
		console.log('searching for', search_term);
		// remove the search term from the url
		let url = window.location.href;
		let split_url = url.split('?');
		let base_url = split_url[0];
		let query_params = split_url[1];
		let url_params = new URLSearchParams(query_params);
		url_params.set(SEARCH_QUERY_PARAM, search_term);
		url = `${base_url}?${url_params.toString()}`;
		location = url;
	}

	function preform_sort(field, current_field_key) {
		console.log('preform_sort', field, current_field_key);
		if (field.sortable === true) {
			const url_params = new URLSearchParams(window.location.search);
			const ordering = url_params.get(ORDERING_QUERY_PARAM) || '';
			const ordering_fields = ordering.split(',');
			let new_ordering = '';
			let field_key = '';
			let found = false;
			for (const field of ordering_fields) {
				if (field === '') continue;
				if (field.startsWith('-')) {
					field_key = field.slice(1);
				} else {
					field_key = field;
				}
				if (field_key === current_field_key) {
					found = true;
					if (field.startsWith('-')) {
						new_ordering += field_key;
					} else {
						new_ordering += '-' + field_key;
					}
				} else {
					new_ordering += field;
				}
				new_ordering += ',';
			}
			if (!found) {
				if (field.sorted === 'asc') {
					new_ordering += '-' + current_field_key + ',';
				} else {
					new_ordering += current_field_key + ',';
				}
			}
			// remove last comma
			new_ordering = new_ordering.slice(0, -1);
			// set the ordering to the url_params
			url_params.set(ORDERING_QUERY_PARAM, new_ordering);

			location.href = `${$page.url.pathname}?${url_params.toString()}`;
		}
	}

	function remove_from_sort(field, current_field_key) {
		const url_params = new URLSearchParams(window.location.search);
		const ordering = url_params.get(ORDERING_QUERY_PARAM) || '';
		const ordering_fields = ordering.split(',');
		let new_ordering = '';
		let field_key = '';
		let found = false;
		for (const field of ordering_fields) {
			if (field === '') continue;
			if (field.startsWith('-')) {
				field_key = field.slice(1);
			} else {
				field_key = field;
			}
			if (field_key === current_field_key) {
				found = true;
			} else {
				new_ordering += field;
			}
			new_ordering += ',';
		}
		// remove comma at the end
		if (new_ordering.endsWith(',')) {
			new_ordering = new_ordering.slice(0, -1);
		}
		url_params.set(ORDERING_QUERY_PARAM, new_ordering);
		location.href = `${$page.url.pathname}?${url_params.toString()}`;
	}
	const dispatch = createEventDispatcher();
	function expendable_button_click(row, index) {
		expended_rows[row.id] = !expended_rows[row.id];
		dispatch('expended_row_click', {
			row: row,
			expended: expended_rows[row.id],
			index: index
		});
	}
	export let user_cell_components = {};
	let custom_cell_components = {
		'test-component': TestCustomCell,
		'awaiting-projects-action-cell': AwaitingProjectsActionCell,
		'projects-action-cell': ProjectsActionCell,
		'awaiting-projects-alert-date-cell': AwaitingProjectsAlertDateCell,
		'projects-progress-cell': ProjectsProgressCell,
		...user_cell_components
	};
</script>

<div class="col-9 main-area">
	<!-- pagination results -->
	{#if pagination}
		<PaginationResult {api_data} />
	{/if}
	{#if show_search_bar}
		<!-- search box -->
		<div class="d-flex justify-content-center px-5">
			<div class="search">
				<input
					type="text"
					class="search-input"
					placeholder="חיפוש..."
					name=""
					bind:value={search_term}
					on:keypress={search_on_enter}
				/>
				<button class="search-icon" on:click={preform_search}> <i class="fa fa-search" /> </button>
			</div>
		</div>
	{/if}
	{#if description && api_data}
		<div class="scroll-table" style="--table-height: {table_height_px}">
			<table class="table table-bordered table-hover table-striped">
				<thead class="thead-dark">
					<tr>
						{#if expendable}
							<th class="expender-td" />
						{/if}
						<!-- <th>#</th> -->
						{#if allow_select}
							<th>
								<input
									class="form-check-input"
									type="checkbox"
									value=""
									id="flexCheckDefault"
									on:change={select_all_rows}
									bind:checked={select_all}
								/>
							</th>
						{/if}
						{#each Object.keys(description['api-description'].fields) as field_key, i}
							{@const field = description['api-description'].fields[field_key]}
							<th>
								<button class="btn transparent-btn" on:click={() => preform_sort(field, field_key)}>
									{field.lable}

									{#if field.sortable}
										{#if field.sorted === 'asc'}
											<svg
												xmlns="http://www.w3.org/2000/svg"
												width="16"
												height="16"
												fill="currentColor"
												class="bi bi-caret-up-fill"
												viewBox="0 0 16 16"
											>
												<path d="M8 4.879 3.5 9h9L8 4.879z" />
											</svg>
										{:else if field.sorted === 'desc'}
											<svg
												xmlns="http://www.w3.org/2000/svg"
												width="16"
												height="16"
												fill="currentColor"
												class="bi bi-caret-down-fill"
												viewBox="0 0 16 16"
											>
												<path d="M8 11.121 12.5 7H3.5L8 11.121z" />
											</svg>
										{/if}
										{#if field?.sort_order != undefined}
											<small class="text-muted" title="מיקום במיון">{field.sort_order + 1}</small>
										{/if}
									{/if}
								</button>
								{#if field.sortable && field.sorted}
									<button
										class="btn btn-secondary btn-sm"
										on:click={() => remove_from_sort(field, field_key)}
									>
										הסר מיון
									</button>
								{/if}
							</th>
						{/each}
					</tr>
				</thead>
				<tbody class="table-group-divider">
					{#each api_data.results as row, i}
						<tr>
							{#if expendable}
								<td class="expender-td">
									<button
										type="button"
										aria-expanded={expended_rows[row.id]}
										on:click={() => {
											expendable_button_click(row, i);
										}}
										class="btn expender-btn"
									>
										<svg
											width="40px"
											height="40px"
											viewBox="0 0 24 24"
											fill="none"
											xmlns="http://www.w3.org/2000/svg"
										>
											<path
												d="M16.0686 9H7.9313C7.32548 9 7.02257 9 6.88231 9.1198C6.76061 9.22374 6.69602 9.37967 6.70858 9.53923C6.72305 9.72312 6.93724 9.93731 7.36561 10.3657L11.4342 14.4343C11.6322 14.6323 11.7313 14.7313 11.8454 14.7684C11.9458 14.8011 12.054 14.8011 12.1544 14.7684C12.2686 14.7313 12.3676 14.6323 12.5656 14.4343L16.6342 10.3657C17.0626 9.93731 17.2768 9.72312 17.2913 9.53923C17.3038 9.37967 17.2392 9.22374 17.1175 9.1198C16.9773 9 16.6744 9 16.0686 9Z"
												stroke="#000000"
												stroke-width="2"
												stroke-linecap="round"
												stroke-linejoin="round"
											/>
										</svg>
									</button>
								</td>
							{/if}
							<!-- <td>{i + 1}</td> -->
							{#if allow_select}
								<td>
									<input
										class="form-check-input"
										type="checkbox"
										value=""
										id="flexCheckDefault"
										on:change={() => select_row(row)}
										bind:checked={selected_ids[row.id]}
									/>
								</td>
							{/if}
							{#each Object.keys(description['api-description'].fields) as field_key}
								<td>
									<div class="my-td">
										{#if description['api-description'].fields[field_key].type === 'datetime'}
											<HebrewDateTimeCell data={row[field_key]} />
										{:else if description['api-description'].fields[field_key].type === 'date'}
											<HebrewDateCell data={row[field_key]} />
										{:else if description['api-description'].fields[field_key].type === 'currency'}
											<CurrencyCell data={row[field_key]} />
										{:else if description['api-description'].fields[field_key].type === 'custom'}
											<svelte:component
												this={custom_cell_components[
													description['api-description'].fields[field_key].custom_component
												]}
												data={{
													row: row,
													field_key: field_key,
													description: description,
													api_data: api_data
												}}
											/>
										{:else}
											<RawCell data={row[field_key]} />
										{/if}
									</div>
								</td>
							{/each}
						</tr>
						{#if expendable}
							<tr class="expended-row" class:expanded={expended_rows[row.id]}>
								<td colspan={Object.keys(description['api-description'].fields).length + 1}>
									{#if expended_rows[row.id]}
										<div class="expended-row-content">
											<slot
												name="expended-row-content"
												{row}
												row_index={i}
												show={expended_rows[row.id] === true}
											>
												{row.id}
											</slot>
										</div>
									{/if}
								</td>
							</tr>
						{/if}
					{/each}
				</tbody>
			</table>
		</div>
	{:else}
		<div class="spinner-border" role="status">
			<span class="sr-only" />
		</div>
	{/if}
</div>

<BulkActions bind:actions {selected_data} {clear_select} />

<style lang="scss">
	.expender-td,
	.expender-th {
		width: 40px;
		height: 40px;
	}
	.expender-td {
		padding: 0px;
	}
	button.expender-btn {
		background-color: transparent;
		border: none;
		padding: 0;
		width: 40px;
		height: 40px;

		text-align: center;
		text-indent: 0;
		transform: rotate(90deg);
		svg {
			fill: #fff;
			transition: transform 0.25s ease-in;
			transform-origin: center 45%;
		}
		&[aria-expanded='true'] svg {
			transform: rotate(-90deg);
		}
	}

	table.table {
		table-layout: fixed;
		thead {
			tr {
				th {
					text-align: center;
				}
			}
		}
		tbody {
			tr {
				td {
					.my-td {
						display: flex;
						justify-content: center;
						align-items: center;
						text-align: center;
					}
				}

				&.expended-row {
					display: none;
					&.expanded {
						display: table-row;
					}
				}
			}
		}
	}
	.scroll-table {
		overflow-y: auto;
		height: var(--table-height);
	}
	.main-area {
		background-color: #f5f5f5;
		padding: 1rem;
	}

	.search {
		width: 100%;
		margin-bottom: auto;
		margin-top: 20px;
		height: 50px;
		background-color: #fff;
		padding: 10px;
		border-radius: 5px;
		margin-bottom: 20px;
	}
	.search-input {
		color: white;
		border: 0;
		outline: 0;
		background: none;
		width: 0;
		margin-top: 5px;
		caret-color: transparent;
		// line-height: 20px;
		transition: width 0.4s linear;
		padding: 0 10px;
		width: 100%;
		caret-color: #536bf6;
		// font-size: 19px;
		font-weight: 300;
		color: black;
		transition: width 0.4s linear;
	}

	.search-icon {
		border: none;
		height: 34px;
		width: 34px;
		float: left;
		display: flex;
		justify-content: center;
		align-items: center;
		color: white;
		background-color: #536bf6;
		font-size: 10px;
		bottom: 30px;
		position: relative;
		border-radius: 5px;
	}

	.search-icon:hover {
		background-color: #6c80f4;
	}

	.search-icon:hover {
		color: #fff !important;
	}

	a:link {
		text-decoration: none;
	}
</style>
