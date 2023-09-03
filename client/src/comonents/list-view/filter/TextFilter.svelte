<script>
	export let title;
	export let slug;
	export let value = '';

	export function reset_filter() {
		value = '';
	}

	export function get_query_param() {
		if (value) {
			return [{ name: slug, value: value }];
		}
		return [{ name: slug, value: '' }];
	}

	export function set_from_url(url) {
		const url_params = new URLSearchParams(url.split('?')[1]);
		value = url_params.get(slug);
	}
</script>

<div class="form-group">
	<label for={slug}>{title}</label>
	<input type="text" class="form-control" id={slug} placeholder={title} bind:value />
</div>
