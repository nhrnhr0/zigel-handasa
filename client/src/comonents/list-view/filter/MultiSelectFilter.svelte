<script>
	import MultiSelect from 'svelte-multiselect';

	export let title;
	export let slug;
	export let options;
	export let value = undefined;

	export function reset_filter() {
		value = undefined;
	}

	export function get_query_param() {
		if (value && value.length > 0) {
			let ids = value.map((item) => item.value);
			// return `${slug}__in=${ids.join(',')}`;
			return [{ name: slug + '__in', value: ids.join(',') }];
		}
		return [{ name: slug + '__in', value: '' }];
	}

	export function set_from_url(url) {
		const url_params = new URLSearchParams(url.split('?')[1]);
		let ids = url_params.get(slug + '__in');
		if (ids) {
			ids = ids.split(',');
			// convert to int
			ids = ids.map((item) => parseInt(item));
			value = options.filter((item) => ids.includes(item.value));
		}
	}
</script>

<div class="form-group">
	<label for={slug}>{title}</label>
	<MultiSelect bind:value {options} />
</div>
