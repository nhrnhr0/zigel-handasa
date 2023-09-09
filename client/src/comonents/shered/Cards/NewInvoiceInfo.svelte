<script>
	import { MultiSelect } from 'svelte-multiselect';
	import DocumentIncomeTable from '../../DocumentIncomeTable.svelte';
	import { onMount } from 'svelte';

	export let form_data;
</script>

<div class="card doc-info-card" style="border-top: none; margin-top: 0px;">
	<div class="card-body">
		<h4 class="form-title" id="userInfoHeader">פרטי המסמך</h4>
		<div class="row form-group">
			<div class="col-6">
				<label for="fname">שם הלקוח *</label>
				<MultiSelect
					disabled={true}
					options={[]}
					maxSelect={1}
					selected={[{ label: form_data.client.recipient.name, value: 0 }]}
				/>
			</div>

			<div class="col-3">
				<label for="documentDate">תאריך המסמך *</label>
				<input
					class="form-control"
					type="date"
					id="documentDate"
					name="documentDate"
					placeholder="בחרו תאריך"
					bind:value={form_data.date}
				/>
			</div>
			<div class="col-3">
				<label for="documentDate">לתשלום עד *</label>
				<input
					class="form-control"
					type="date"
					id="documentDate"
					name="documentDate"
					placeholder="בחרו תאריך"
					bind:value={form_data.dueDate}
				/>
			</div>
		</div>
	</div>
</div>
<pre>
    {JSON.stringify(form_data, null, 2)}
</pre>
<!--
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
				/>
			</div>
		</div>
	</div>
</div>
-->
