<script>
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
			}
			if (value['to']) {
				ret.push({ name: `${slug}__lte`, value: value['to'] });
			}
		}
		return ret;
	}

	export function set_from_url(url) {
		const url_params = new URLSearchParams(url.split('?')[1]);
		value['from'] = url_params.get(`${slug}__gte`);
		value['to'] = url_params.get(`${slug}__lte`);
	}
</script>

<div class="form-group">
	<!-- from date to date -->
	<label for={slug}>{title}</label>
	<div class="input-group">
		<div class="input-group-preappend">
			<span class="input-group-text">מ</span>
		</div>
		<input
			type="date"
			class="form-control"
			id={slug}
			placeholder={title}
			bind:value={value['from']}
		/>

		<div class="input-group-append">
			<span class="input-group-text">עד</span>
		</div>
		<input
			type="date"
			class="form-control"
			id={slug}
			placeholder={title}
			bind:value={value['to']}
		/>
	</div>
</div>
