<script>
	export let data;

	function go_to_project() {
		window.location.href = `/done-projects/${data.row.id}`;
	}
</script>

<td>
	<ul class="list-inline m-0">
		<li class="list-inline-item">
			<!-- edit -->

			<button
				on:click={go_to_project}
				class="btn btn-secondary btn-sm rounded-0"
				type="button"
				data-toggle="tooltip"
				data-placement="top"
				title="Edit"><i class="fa fa-edit" /></button
			>
		</li>
	</ul>
</td>

<style lang="scss">
	ul.list-inline {
		padding: 0px;
	}
</style>
