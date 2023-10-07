<script>
	import Tabs from './../shered/Tabs.svelte';
	import PricePropInfo from './../shered/Cards/PricePropInfo.svelte';
	import CommentsCard from './../shered/Cards/CommentsCard.svelte';
	import Flatpickr from './../shered/flatpicker/Flatpickr.svelte';
	import { network_approve_rejected_project } from '$lib/network.js';
	import { notifier } from '@beyonk/svelte-notifications';
	import { goto } from '$app/navigation';
	export let form_data;
	export let on_update_function;
	let activeTabId;

	let updateing = false;
	function save_form_data(e) {
		e.preventDefault();
		updateing = true;
		let ret_url = '/rejected-project/';
		if (e.target.value == 'saveAndContinue') {
			ret_url += form_data.id;
		}
		on_update_function(form_data.id, form_data, ret_url).then((res) => {
			updateing = false;
		});
	}
	function handleApproveClick() {
		// openModal(ModalApprove, { awaiting_project_id: form_data.id });
		network_approve_rejected_project(form_data.id).then((res) => {
			if (res.status == 200) {
				notifier.success('הפרויקט אושר בהצלחה', {
					// position: 'bottom-right',
					timeout: 3000
				});
				goto('/rejected-project');
			} else {
				notifier.danger('אירעה שגיאה בעת אישור הפרויקט', {
					// position: 'bottom-right',
					timeout: 3000
				});
			}
		});
	}
</script>

<div class="container">
	<h1 id="FirstHeader">הצעת מחיר {form_data.api_data['number']}</h1>
	<form class="price-proposal-form">
		<Tabs
			bind:activeTabId
			items={[
				{ id: 1, label: 'פרטי המסמך', selected: true },
				{ id: 2, label: 'הערות + הפעל פרויקט', selected: false },
				{ id: 3, label: 'קבצים', selected: false }
			]}
		/>
		{#if activeTabId == 1}
			<PricePropInfo bind:form_data />
		{/if}
		{#if activeTabId == 2}
			<div class="card awaiting-project-info" style="border-top: none; margin-top: 0px;">
				<div class="card-body">
					<h4 class="form-title" id="userInfoHeader">הערות + הפעל פרויקט</h4>
					<div class="row">
						<CommentsCard bind:comments={form_data.comments} />
					</div>

					<div class="row">
						<div class="col">
							<!-- button to activate project -->
							<button class="btn btn-primary" on:click={handleApproveClick}> הפעל פרויקט </button>
						</div>
					</div>
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
