<script>
	import Tabs from './shered/Tabs.svelte';
	import PricePropInfo from './shered/Cards/PricePropInfo.svelte';
	import CommentsCard from './shered/Cards/CommentsCard.svelte';
	import { MultiSelect } from 'svelte-multiselect';
	import UploadFilesTab from './upload-fiels/uploadFilesTab.svelte';
	export let form_data;
	export let original_data;
	export let on_update_function;
	let activeTabId;

	let updateing = false;
	function save_form_data(e) {
		e.preventDefault();
		if (original_data == undefined) {
			original_data = JSON.parse(JSON.stringify(form_data));
		}
		// if the total is diffrent from the original total
		// we prompt the user to confirm the change and resend the price proposal to the client
		if (form_data.total != original_data.total) {
			if (confirm('האם ברצונך לשלוח מחיר חדש ללקוח?')) {
				// send the price proposal to the client
				form_data.resend_price_proposal = true;
			} else {
				// don't send the price proposal to the client
				form_data.resend_price_proposal = false;
			}
		} else {
			form_data.resend_price_proposal = false;
		}
		updateing = true;
		on_update_function(form_data.id, form_data).then((res) => {
			updateing = false;
		});
	}

	function end_project() {}
</script>

<div class="container">
	<h1 id="FirstHeader">פרויקט {form_data.api_data['number']}</h1>
	<form class="price-proposal-form">
		<Tabs
			bind:activeTabId
			items={[
				{ id: 1, label: 'פרטי המסמך', selected: true },
				{ id: 2, label: 'הערות + סטטוס', selected: false },
				{ id: 3, label: 'קבצים', selected: false }
			]}
		/>
		{#if activeTabId == 1}
			<PricePropInfo bind:form_data />
		{/if}
		{#if activeTabId == 2}
			<div class="card awaiting-project-info" style="border-top: none; margin-top: 0px;">
				<div class="card-body">
					<h4 class="form-title" id="userInfoHeader">הערות + תאריך התראה</h4>
					<div class="row">
						<div class="col">
							<div class="form-group">
								<label for="status">סטטוס</label>
								<MultiSelect
									outerDivClass="status-select"
									options={form_data.status_options}
									maxSelect={1}
									bind:selected={form_data.status}
									allowUserOptions={true}
									createOptionMsg={'הוסף סטטוס חדש'}
								/>
							</div>
						</div>
						<div class="col">
							<div class="form-group">
								<label for="order_number">מספר הזמנה במערכת הלקוח</label>
								<input
									type="text"
									class="form-control"
									id="order_number"
									bind:value={form_data.order_number}
								/>
							</div>
						</div>
						<div class="col">
							<div class="form-group">
								<br />
								<div class="form-check form-switch">
									<input
										class="form-check-input"
										type="checkbox"
										role="switch"
										id="flexSwitchCheckChecked"
										bind:checked={form_data.closed}
									/>
									<label class="form-check-label" for="flexSwitchCheckChecked"> סגור פרויקט </label>
								</div>
							</div>
						</div>
					</div>
					<CommentsCard bind:comments={form_data.comments} />
					<br />
				</div>
			</div>
		{/if}
		{#if activeTabId == 3}
			<div class="card awaiting-project-info" style="border-top: none; margin-top: 0px;">
				<div class="card-body">
					<h4 class="form-title" id="userInfoHeader">קבצים</h4>
					<div class="row">
						<div class="col">
							<!-- files -->
							<UploadFilesTab project_id={form_data.id} />
						</div>
					</div>
				</div>
			</div>
		{/if}

		<!-- save button -->
		<div class="row">
			<div class="col">
				<button
					class="btn btn-primary"
					type="submit"
					on:click={save_form_data}
					disabled={updateing}
				>
					{#if updateing}
						<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true" />
						<span class="sr-only">Loading...</span>
					{:else}
						שמור
					{/if}</button
				>
			</div>
		</div>
	</form>
</div>

<style lang="scss">
	:global(.status-select) {
		padding: 0px !important;
		height: 38px !important;
	}
	.price-proposal-form {
		.card {
			margin-bottom: 25px;
		}
	}

	.page-actions {
		margin: auto;
		margin-top: 1rem;
		max-width: 300px;

		.buttons-wraper {
			display: flex;
			justify-content: space-between;
		}
	}
</style>
