<script>
	import DocumentIncomeTable from './DocumentIncomeTable.svelte';
	import MultiSelect from 'svelte-multiselect';
	import { network_update_awaiting_project } from '$lib/network.js';
	import { fly } from 'svelte/transition';
	import Tabs from './shered/Tabs.svelte';
	let client_options = [];
	export let form_data;
	export let on_update_function;
	let activeTabId;
	let new_comment;

	let client = [form_data.client];
	$: {
		form_data.client = client[0];
	}
	let updateing = false;
	function save_form_data(e) {
		e.preventDefault();
		updateing = true;
		on_update_function(form_data.id, form_data).then((res) => {
			updateing = false;
		});
	}

	// {"id": "624d873b-e3a7-461f-9d82-296ef33ae01e", "type": 10, "number": 351, "currency": "ILS", "date": "2023-09-04", "createdAt": 1693808761000, "subtotal": 60.85, "rounding": false, "tax": [{"name": "VAT", "rate": 0.17, "total": 10.35}], "total": 71.2, "description": "gggggg", "remarks": "", "reverseCharge": false, "recipient": {"id": "888e2ac1-3a6f-476d-a948-0b2dfb24afb5", "name": "ffffff", "department": "", "address": "", "city": "", "zip": "", "country": "IL", "phone": "", "mobile": "", "emails": []}, "items": [{"description": "מוצר שמור 02", "sku": "002", "quantity": 3, "price": 15, "currency": "ILS", "taxIncludedInPrice": false, "tax": [{"name": "VAT", "rate": 0.17}]}, {"description": "54", "sku": "44", "quantity": 1, "price": 1, "currency": "ILS", "taxIncludedInPrice": true, "tax": [{"name": "VAT", "rate": 0.17}]}, {"description": "מוצר שמור 02", "sku": "002", "quantity": 1, "price": 15, "currency": "ILS", "taxIncludedInPrice": false, "tax": [{"name": "VAT", "rate": 0.17}]}], "transactions": [], "files": {"signed": true, "downloadLinks": {"he": "https://sandbox.d.greeninvoice.co.il/api/v1/documents/download?d=mTkSvpFaMYB2SCVYrY8NbaYleHCWAee3uuhPI0hmW69EpLf6uisTU3zRgwj0wGkF38YMkHbIcPrJWMstgDcSNuZ6OVY3ZDiVcb2z681bRJe%2FN2DS5wPMtve9x7NHAE7C%2FD5WUvxHN69QB7ofn0LT2dq3ney8Faxlq%2F3Muu7mJcVLcaWwL%2BgzZzERDfxYVuSIG%2B9rxUtOnH2L9fzJhiI%3D", "origin": "https://sandbox.d.greeninvoice.co.il/api/v1/documents/download?d=lVliotWY7jp%2FooUpUc6CvEiJPfg%2BUs%2F3Bc3hkpQ8%2BFqtPA9RU7vAQOyYv9I894ggJcplvHGCpHLwETDFw%2Bdx3PDUmpAsStPLj%2By1L%2Bbhipa4P3qn%2BgDgRipFt3fvpB%2FCVGel73dvWs3cbNIYKUvNi7JKH7Saxl7WV%2BmC76ALLpWxPoIAuo5P320GL9mtMARmzauKJU9I78E8Ao3UTjI%3D"}}}
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
			<div class="card doc-info-card" style="border-top: none; margin-top: 0px;">
				<div class="card-body">
					<h4 class="form-title" id="userInfoHeader">פרטי המסמך</h4>
					<div class="row form-group">
						<div class="col-8">
							<label for="fname">שם הלקוח *</label>
							<!-- <input
							class="form-control"
							type="text"
							id="fname"
							name="fname"
							placeholder="הקלידו את שם הלקוח(שמור)"
							required
						/> -->
							<MultiSelect
								options={form_data.client_options}
								maxSelect={1}
								bind:selected={client}
							/>
						</div>
						<div class="col-4">
							<label for="documentDate">תאריך המסמך *</label>
							<input
								class="form-control"
								type="date"
								id="documentDate"
								name="documentDate"
								placeholder="בחרו תאריך"
								bind:value={form_data.api_data.date}
							/>
						</div>
						<!-- <div class="col">
						<label for="ToPayUntil">לתשלום עד *</label>
						<input
							class="form-control"
							type="date"
							id="ToPayUntil"
							name="ToPayUntil"
							placeholder="בחרו תאריך"
						/>
					</div> -->
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
								bind:value={form_data.name}
							/>
						</div>
					</div>
					<br />
					<div class="row form-group">
						<h4 class="form-title">פירוט שירותים ופריטים</h4>
						<!-- headers -->
						<div class="container">
							<DocumentIncomeTable bind:form_data />
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
								bind:value={form_data.api_data.remarks}
							/>
						</div>
						<!-- <div class="col">
						<label for="footer"> הערות בתחתית המסמך </label>
						<textarea
							class="form-control"
							id="fotter"
							name="fotter"
							rows="3"
							placeholder="מתאים לאותיות קטנות, תנאים ודיסקליימר"
						/>
					</div> -->
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
								bind:selected={form_data.api_data.recipient.emails}
								maxSelect={5}
								duplicateOptionMsg={'המייל כבר קיים'}
							/>
						</div>
						<!--<br />
					 <div class="col">
						<label for="email-content">תוכן נוסף במייל ללקוח</label>
						<textarea
							class="form-control"
							id="email-content"
							name="email-content"
							rows="1"
							placeholder="יצורף לגוף המייל הנשלח ללקוח"
						/>
					</div> -->
					</div>
				</div>
			</div>
		{/if}
		{#if activeTabId == 2}
			<div class="card awaiting-project-info" style="border-top: none; margin-top: 0px;">
				<div class="card-body">
					<div class="row">
						<div class="col">
							<label for="alert_date">תאריך התראה</label>
							<input
								class="form-control"
								type="datetime-local"
								id="alert_date"
								name="alert_date"
								placeholder="בחרו תאריך"
								bind:value={form_data.alert_date}
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
						<div class="col-4">
							<!-- comments -->
							<div class="row">
								<div class="form-group">
									<label for="comments">הערה חדשה</label>
									<textarea
										class="form-control"
										id="comments"
										name="comments"
										rows="3"
										placeholder="הערות נוספות"
										bind:value={new_comment}
									/>
								</div>
							</div>
							<br />
							<div class="row">
								<div class="form-group">
									<button
										class="btn btn-secondary add-comment-btn"
										disabled={!new_comment}
										on:click={(e) => {
											e.preventDefault();
											form_data.comments.unshift({
												comment: new_comment,
												created_at: new Date()
											});
											new_comment = '';
											form_data.comments = [...form_data.comments];
										}}
									>
										הוסף הערה
									</button>
								</div>
							</div>
							<br />
							{#each form_data.comments as comment}
								<div class="card">
									<div class="card-body">
										<div class="row">
											<div class="col" style="white-space: pre-line;">
												{comment.comment}
											</div>
										</div>
										<div class="row">
											<div class="col">
												- {new Date(comment.created_at).toLocaleString('he-IL', {
													timeZone: 'Asia/Jerusalem'
												})}
											</div>
										</div>
										<div class="row">
											- לפני {Math.floor(
												(new Date().setHours(0, 0, 0, 0) -
													new Date(comment.created_at).setHours(0, 0, 0, 0)) /
													(1000 * 60 * 60 * 24)
											)} ימים
										</div>
									</div>
								</div>
							{/each}
						</div>
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
	.price-proposal-form {
		.card {
			margin-bottom: 25px;
		}
	}
	.settings-card-content {
		display: flex;
		flex-direction: row;
		justify-content: space-between;
		align-items: center;

		.settings-results {
			flex: 4;
			display: flex;
			flex-direction: row;
			justify-content: space-between;
			flex-wrap: wrap;
			.settings-result {
				display: flex;
				flex-direction: row;
				justify-content: space-between;
				align-items: center;
				margin: 1rem;
				.settings-result-title {
					margin-right: 20px;
					font-weight: bold;
				}
			}
		}
		.settings-button {
			// flex: 1;
			margin-right: 20px;
		}
	}
</style>
