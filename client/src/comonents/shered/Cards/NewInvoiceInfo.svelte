<script>
	import { MultiSelect } from 'svelte-multiselect';
	import DocumentIncomeTable from '../../DocumentIncomeTable.svelte';
	import { network_create_invoice_from_price_proposals } from '$lib/network.js';
	import { onMount } from 'svelte';
	import Flatpickr from '../flatpicker/Flatpickr.svelte';
	import { notifier } from '@beyonk/svelte-notifications';
	export let title;
	let updateing = false;

	export let form_data;
	export let client_data;

	export function create_invoice() {
		updateing = true;
		debugger;
		console.log('form_data', form_data);
		console.log('client_data', client_data);
		network_create_invoice_from_price_proposals(form_data).then((res) => {
			res.json().then((data) => {
				console.log('data', data);
				updateing = false;
				if (data?.error) {
					// addNotification({
					// 	position: 'bottom-right',
					// 	type: 'error',
					// 	text: data.error,
					// 	removeAfter: 5000
					// });
					notifier.danger(data.error, {
						timeout: 5000, // milliseconds
						persist: false // automatic timeout (ignores above)
					});
				} else {
					alert('המסמך נוצר בהצלחה');
				}
			});
		});
	}
</script>

<div class="container">
	<div class="card doc-info-card" style="border-top: none; margin-top: 0px;">
		<h1>{title}</h1>
		<div class="card-body">
			<h4 class="form-title" id="userInfoHeader">פרטי המסמך</h4>
			<div class="row form-group">
				<div class="col-6">
					<label for="fname">שם הלקוח *</label>
					<MultiSelect
						disabled={true}
						options={[]}
						maxSelect={1}
						selected={[{ label: client_data.name, value: 0 }]}
					/>
				</div>

				<div class="col-3">
					<label for="documentDate">תאריך המסמך *</label>
					<!-- <input
					class="form-control"
					type="date"
					id="documentDate"
					name="documentDate"
					placeholder="בחרו תאריך"
					bind:value={form_data.date}
				/> -->
					<Flatpickr
						class="form-control"
						options={{
							dateFormat: 'Y/m/d',
							altInput: true,
							altFormat: 'd/m/Y',
							enableTime: false,
							defaultDate: form_data.date
						}}
						bind:formattedValue={form_data.date}
					/>
				</div>
				<div class="col-3">
					<label for="documentDate">לתשלום עד *</label>
					<!-- <input
					class="form-control"
					type="date"
					id="documentDate"
					name="documentDate"
					placeholder="בחרו תאריך"
					bind:value={form_data.dueDate}
				/> -->
					<Flatpickr
						class="form-control"
						options={{
							dateFormat: 'Y/m/d',
							altInput: true,
							altFormat: 'd/m/Y',
							enableTime: false,
							defaultDate: form_data.dueDate
						}}
						bind:formattedValue={form_data.dueDate}
					/>
				</div>
			</div>
			<br />
			<div class="row form-group">
				<div class="col">
					<h4 class="form-title">תיאור תכולת המסמך</h4>
					<input
						class="form-control"
						type="text"
						id="SecondUserInfoHeaderText"
						name="SecondUserInfoHeaderText"
						placeholder="למשל, שם הפרויקט"
						bind:value={form_data.description}
					/>
				</div>
				<div class="row form-group">
					<h4 class="form-title">פירוט שירותים ופריטים</h4>
					<div class="container">
						<DocumentIncomeTable
							bind:items={form_data.income}
							bind:discount={form_data.discount}
							bind:tax={form_data.tax}
							bind:total={form_data.total}
							bind:subtotal={form_data.subtotal}
						/>
					</div>
				</div>
			</div>
		</div>
	</div>

	<div class="card form-document-create__remarks">
		<div class="card-body">
			<div class="row">
				<h4 class="form-title">הערות שיופיעו במסמך</h4>
				<div class="col">
					<label for="remarks">תוכן מתחת לשורות הפירוט </label>
					<textarea
						class="form-control"
						id="remarks"
						name="remarks"
						rows="3"
						placeholder="יוצג ליד שורת הפירוט, בסמוך לחתימה שלך"
						bind:value={form_data.remarks}
					/>
				</div>
				<div class="col">
					<label for="footer"> הערות בתחתית המסמך </label>
					<textarea
						class="form-control"
						id="fotter"
						name="fotter"
						rows="3"
						placeholder="מתאים לאותיות קטנות, תנאים ודיסקליימר"
					/>
				</div>
			</div>
		</div>
	</div>

	<div class="form-document-create__email card">
		<div class="card-body">
			<h4 class="form-title">שליחה במייל</h4>

			<div class="container">
				<div class="col">
					<label for="client-emails"> שליחת מסמך המקור במייל </label>
					<MultiSelect
						options={[]}
						allowUserOptions={'apppend'}
						createOptionMsg={'הוספת מייל חדש'}
						bind:selected={form_data.client.emails}
						maxSelect={5}
						duplicateOptionMsg={'המייל כבר קיים'}
					/>
				</div>
				<br />
				<div class="col">
					<label for="email-content">תוכן נוסף במייל ללקוח</label>
					<textarea
						class="form-control"
						id="email-content"
						name="email-content"
						rows="1"
						placeholder="יצורף לגוף המייל הנשלח ללקוח"
					/>
				</div>
			</div>
		</div>

		<!-- save button -->
		<div class="row">
			<div class="col">
				<button
					class="btn btn-primary"
					type="submit"
					disabled={updateing}
					on:click={create_invoice}
				>
					{#if updateing}
						<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true" />
						<span class="sr-only">Loading...</span>
					{:else}
						הפק מסמך
					{/if}</button
				>
			</div>
		</div>
	</div>
</div>
