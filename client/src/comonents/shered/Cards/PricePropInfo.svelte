<script>
	import { MultiSelect } from 'svelte-multiselect';
	import DocumentIncomeTable from '../../DocumentIncomeTable.svelte';

	export let form_data;
</script>

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
					disabled={true}
					options={form_data.client_options}
					maxSelect={1}
					bind:selected={form_data.client}
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
				<DocumentIncomeTable
					bind:items={form_data.api_data.items}
					bind:discount={form_data.api_data.discount}
					bind:tax={form_data.api_data.tax}
					bind:total={form_data.api_data.total}
					bind:subtotal={form_data.api_data.subtotal}
				/>
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
			<div class="col">
				<label for="footer"> הערות בתחתית המסמך</label>
				<textarea
					class="form-control"
					id="fotter"
					name="fotter"
					rows="3"
					placeholder="מתאים לאותיות קטנות, תנאים ודיסקליימר"
					bind:value={form_data.api_data.footer}
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
					bind:selected={form_data.api_data.recipient.emails}
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
					bind:value={form_data.api_data.recipient.email_content}
				/>
			</div>
		</div>
	</div>
</div>
