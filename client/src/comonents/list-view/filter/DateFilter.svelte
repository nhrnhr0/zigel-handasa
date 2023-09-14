<script>
	import { onMount } from 'svelte';
	import Flatpickr from '../../shered/flatpicker/Flatpickr.svelte';

	export let title;
	export let slug;
	export let value = {};
	export function reset_filter() {
		value = {};
	}

	export function get_query_param() {
		let ret = [];
		if (value) {
			// if (value['from']) {
			// 	query_param += `${slug}__gte=${value['from']}`;
			// }
			// if (value['to']) {
			// 	query_param += `&${slug}__lte=${value['to']}`;
			// }
			if (value['from']) {
				ret.push({ name: `${slug}__gte`, value: value['from'] });
			} else {
				ret.push({ name: `${slug}__gte`, value: '' });
			}
			if (value['to']) {
				ret.push({ name: `${slug}__lte`, value: value['to'] });
			} else {
				ret.push({ name: `${slug}__lte`, value: '' });
			}
		}
		return ret;
	}

	function handleChange_gte(event) {
		const [selectedDates, dateStr] = event.detail;
		console.log({ selectedDates, dateStr });
		value['from'] = dateStr;
	}

	function handleChange_lte(event) {
		const [selectedDates, dateStr] = event.detail;
		console.log({ selectedDates, dateStr });
		value['to'] = dateStr;
	}

	export function set_from_url(url) {
		// 2023-09-08 12:00
		const url_params = new URLSearchParams(url.split('?')[1]);
		value['from'] = url_params.get(`${slug}__gte`);
		value['to'] = url_params.get(`${slug}__lte`);

		// set the value of the flatpickr
		const fp_gte = document.getElementById(`${slug}__gte`);
		const fp_lte = document.getElementById(`${slug}__lte`);

		if (fp_gte && fp_lte) {
			if (value['from']) {
				fp_gte._flatpickr.setDate(value['from'], true, 'Y-m-d H:i');
			}
			if (value['to']) {
				fp_lte._flatpickr.setDate(value['to'], true, 'Y-m-d H:i');
			}
		}
	}
</script>

<div class="form-group">
	<!-- from date to date -->
	<label for={slug}>{title}</label>
	<div class="input-group">
		<div class="input-group-preappend">
			<span class="input-group-text">מ</span>
		</div>
		<Flatpickr
			on:change={handleChange_gte}
			id="{slug}__gte"
			on:close={() => {
				console.log('closed');
			}}
			placeholder="בחר תאריך"
		/>

		<div class="input-group-append">
			<span class="input-group-text">עד</span>
		</div>
		<Flatpickr
			on:change={handleChange_lte}
			id="{slug}__lte"
			on:close={() => {
				console.log('closed');
			}}
			placeholder="בחר תאריך"
		/>
	</div>
</div>
