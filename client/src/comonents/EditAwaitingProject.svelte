<script>
	import Tabs from './shered/Tabs.svelte';
	import PricePropInfo from './shered/Cards/PricePropInfo.svelte';
	import CommentsCard from './shered/Cards/CommentsCard.svelte';
	import ModalApprove from '../modals/awaiting-approval/ModalApprove.svelte';
	import ModalReject from '../modals/awaiting-approval/ModalReject.svelte';
	import { openModal } from 'svelte-modals';
	import UploadFiles from './upload-fiels/uploadFilesTab.svelte'
	import Flatpickr from './shered/flatpicker/Flatpickr.svelte';
	export let form_data;
	export let on_update_function;
	let activeTabId;

	let updateing = false;
	function save_form_data(e) {
		e.preventDefault();
		updateing = true;
		let ret_url = '/waiting-approval/';
		if (e.target.value == 'saveAndContinue') {
			ret_url += form_data.id;
		}
		on_update_function(form_data.id, form_data, ret_url).then((res) => {
			updateing = false;
		});
	}

	function handleApproveClick() {
		openModal(ModalApprove, { awaiting_project_id: form_data.id });
	}

	function handleRejectClick() {
		openModal(ModalReject, { awaiting_project_id: form_data.id });
	}
</script>

<div class="container">
	<h1 id="FirstHeader">הצעת מחיר {form_data.api_data['number']}</h1>
	<form class="price-proposal-form">
		<Tabs
			bind:activeTabId
			items={[
				{ id: 1, label: 'פרטי המסמך', selected: true },
				{ id: 2, label: 'הערות + תאריך התראה', selected: false },
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
							<label for="alert_date">תאריך התראה</label>
							<!-- <input
								class="form-control"
								type="datetime-local"
								id="alert_date"
								name="alert_date"
								placeholder="בחרו תאריך"
								bind:value={form_data.alert_date}
							/> -->
							<Flatpickr
								bind:value={form_data.alert_date}
								options={{
									enableTime: true,
									dateFormat: 'd/m/Y H:i',
									altInput: true,
									altFormat: 'd/m/Y H:i',
									time_24hr: true,
									locale: 'he'
								}}
							/>
							<small>
								צריך ליצור קשר עם הלקוח בעוד: {Math.floor(
									(new Date(form_data.alert_date).setHours(0, 0, 0, 0) -
										new Date().setHours(0, 0, 0, 0)) /
										(1000 * 60 * 60 * 24)
								)} ימים
							</small>
						</div>
					</div>
					<div class="row">
						<div class="page-actions">
							<div class="buttons-wraper">
								<button type="button" class="btn btn-success" on:click={handleApproveClick}>
									סמן כאושר
								</button>
								<button type="button" class="btn btn-danger" on:click={handleRejectClick}>
									סמן כנדחה
								</button>
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
							<UploadFiles project_id={form_data.id} />
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
					value="save"
				>
					שמור
				</button>

				<button
					class="btn btn-primary"
					type="submit"
					on:click={save_form_data}
					value="saveAndContinue"
					disabled={updateing}
				>
					שמור והמשך עריכה
				</button>
			</div>
		</div>
	</form>
</div>

<style lang="scss">
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
