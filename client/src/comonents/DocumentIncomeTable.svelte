<script>
	export let form_data;

	function calculate_item_total(item) {
		let total = (item.price / (item.taxIncludedInPrice ? 1.17 : 1)) * item.quantity;
		return total;
	}

	function add_empty_item() {
		form_data.api_data.items.push({
			description: '',
			sku: '',
			quantity: 1,
			price: '',
			currency: 'ILS',
			taxIncludedInPrice: false,
			tax: [{ name: 'VAT', rate: 0.17 }],
			editable: true
		});
		form_data.api_data.items = [...form_data.api_data.items];
	}

	function set_editable_item(index, editable) {
		form_data.api_data.items[index].editable = editable;
	}

	// listiner to update the form_data.api_data.total, form_data.api_data.subtotal, form_data.api_data.discount.total, form_data.api_data.tax[0].total
	// and init form_data.api_data.discount if it is undefined
	$: {
		// set form_data.api_data.subtotal based on the items
		let subtotal = 0;
		for (const item of form_data.api_data.items) {
			subtotal += calculate_item_total(item);
		}
		form_data.api_data.subtotal = subtotal;
		if (subtotal != 0) {
			if (form_data.api_data.discount == undefined) {
				form_data.api_data.discount = {
					type: 'amount',
					value: '',
					total: 0
				};
			}
		}
		if (
			form_data.api_data.discount.type &&
			form_data.api_data.discount.value == undefined &&
			subtotal != 0
		) {
			if (form_data.api_data.discount.type === 'amount') {
				form_data.api_data.discount.value = -1 * form_data.api_data.discount.total;
			} else {
				form_data.api_data.discount.value =
					-1 * (form_data.api_data.discount.total / subtotal) * 100;
			}
		}
		// set form_data.api_data.discount.total based on the items and form_data.api_data.discount.value
		let val = form_data.api_data.discount.value || 0;
		if (form_data.api_data.discount.type === 'amount') {
			form_data.api_data.discount.total = parseFloat(val).toFixed(2);
		} else {
			form_data.api_data.discount.total = parseFloat((val / 100) * subtotal).toFixed(2);
		}

		// calculate the tax (form_data.api_data.tax[0].total) = (subtotal - form_data.api_data.discount.total) * form_data.api_data.tax[0].rate
		form_data.api_data.tax[0].total = (
			(form_data.api_data.subtotal - form_data.api_data.discount.total) *
			form_data.api_data.tax[0].rate
		).toFixed(2);

		// set the total
		form_data.api_data.total = (
			parseFloat(form_data.api_data.subtotal) -
			parseFloat(form_data.api_data.discount.total) +
			parseFloat(form_data.api_data.tax[0].total)
		).toFixed(2);
	}
</script>

<table class="document-income-table">
	<thead>
		<th style="width: 70px;">
			<div class="description-header">מק"ט</div>
		</th>
		<th style="width: 500px;">
			<div class="description-header">פירוט *</div>
		</th>
		<th style="width: 80px;">
			<div class="description-header">כמות *</div>
		</th>
		<th style="width: 150px;">
			<div class="description-header">מחיר ליחידה *</div>
		</th>
		<th style="width: 150px;">
			<div class="description-header">מטבע</div>
		</th>
		<th>
			<div class="description-header">מע"מ</div>
		</th>
		<th>
			<div class="description-header">סה"כ</div>
		</th>
		<th>
			<div class="description-header" />
		</th>
	</thead>
	<tbody>
		{#each form_data.api_data.items as item, i}
			{#if item.editable}
				<tr class="editable-row" id="editable-row-{i}">
					<td>
						<input
							class="form-control"
							type="text"
							id="CatalogNumber"
							name="CatalogNumber"
							bind:value={item.sku}
						/>
					</td>
					<td>
						<input
							class="form-control description"
							type="text"
							id="Description"
							name="Description"
							bind:value={item.description}
						/>
					</td>
					<td>
						<input
							class="form-control quantity"
							type="text"
							id="Amount"
							name="Amount"
							bind:value={item.quantity}
						/>
					</td>
					<td>
						<input
							class="form-control price"
							type="text"
							id="Price per unit"
							name="Price per unit"
							bind:value={item.price}
						/>
					</td>
					<td>
						<select id="secondCurrencyOptions" class="form-control" bind:value={item.currency}>
							<option value="ILS">שקל ישראלי</option>
							<option value="US Dollar">דולר אמריקאי</option>
							<option value="Euro">אירו</option>
						</select>
					</td>
					<td>
						<!-- tax included -->
						<select id="taxIncluded" class="form-control" bind:value={item.taxIncludedInPrice}>
							<option value={false}>לפני</option>
							<option value={true}>כולל</option>
						</select>
					</td>
					<td>
						<div class="description-value">{calculate_item_total(item).toFixed(2)}</div>
					</td>
					<td>
						<div class="my-row">
							<button
								class="btn btn-success"
								on:click={(e) => {
									e.preventDefault();
									debugger;
									// make sure all fields are filled (item.description != '', item.quantity != '', item.price != '')
									// if not, show error message
									// if yes, set editable to false
									if (item.description === '' || item.quantity === '' || item.price === '') {
										// add invalid class to the empty fields
										let tr = window.document.getElementById('editable-row-' + i);

										let description_td = tr.getElementsByClassName('description');
										if (description_td.length > 0) {
											if (item.description === '') {
												description_td[0].classList.add('is-invalid');
											} else {
												description_td[0].classList.remove('is-invalid');
											}
										}

										let quantity_td = tr.getElementsByClassName('quantity');
										if (item.quantity === '') {
											quantity_td[0].classList.add('is-invalid');
										} else {
											quantity_td[0].classList.remove('is-invalid');
										}

										let price_td = tr.getElementsByClassName('price');
										if (item.price === '') {
											price_td[0].classList.add('is-invalid');
										} else {
											price_td[0].classList.remove('is-invalid');
										}
									} else {
										set_editable_item(i, false);
									}
								}}
							>
								שמור</button
							>

							<button
								class="delete-button btn"
								on:click={(e) => {
									e.preventDefault();
									form_data.api_data.items.splice(i, 1);
									form_data.api_data.items = [...form_data.api_data.items];
								}}
							>
								<svg
									data-v-e9de0afc=""
									data-v-23506119=""
									data-v-f1f6c310=""
									xmlns="http://www.w3.org/2000/svg"
									viewBox="0 0 24 24"
									role="presentation"
									width="14"
									height="14"
									aria-labelledby="times"
									transform=""
									><g data-v-e9de0afc="" fill="currentColor"
										><path
											data-v-23506119=""
											data-v-e9de0afc=""
											d="M1.72,0.001c-0.696,0-1.323,0.422-1.584,1.068s-0.108,1.385,0.391,1.87l9.055,9.058l-9.055,9.058
                                c-0.447,0.429-0.627,1.066-0.471,1.666s0.624,1.068,1.224,1.224s1.236-0.024,1.666-0.471L12,14.415l9.055,9.058
                                c0.429,0.447,1.066,0.627,1.666,0.471c0.6-0.156,1.068-0.624,1.224-1.224c0.156-0.6-0.024-1.238-0.471-1.666l-9.055-9.058
                                l9.055-9.058c0.506-0.492,0.658-1.245,0.382-1.894c-0.276-0.65-0.919-1.065-1.625-1.044c-0.444,0.014-0.866,0.199-1.176,0.518
                                L12,9.576L2.945,0.52C2.623,0.187,2.181,0.001,1.72,0.001z"
										/></g
									></svg
								>
							</button>
						</div>
					</td>
				</tr>
			{:else}
				<tr>
					<td>
						<div class="description-value">{item.sku}</div>
					</td>
					<td>
						<div class="description-value">{item.description}</div>
					</td>
					<td>
						<div class="description-value">{item.quantity}</div>
					</td>
					<td>
						<div class="description-value">
							{(item.price / (item.taxIncludedInPrice ? 1.17 : 1)).toFixed(2)}
						</div>
					</td>
					<td>
						<div class="description-value">{item.currency}</div>
					</td>
					<td>
						<div class="description-value">
							{item.taxIncludedInPrice ? 'כולל' : 'לפני'}
						</div>
					</td>
					<td>
						<div class="description-value">{calculate_item_total(item).toFixed(2)}</div>
					</td>
					<td>
						<div class="my-row">
							<button
								class="btn"
								on:click={(e) => {
									debugger;
									set_editable_item(i, true);
									e.preventDefault();
								}}
							>
								<svg
									data-v-e9de0afc=""
									data-v-0531b344=""
									data-v-f1f6c310=""
									xmlns="http://www.w3.org/2000/svg"
									viewBox="0 0 24 24"
									role="presentation"
									width="24"
									height="24"
									aria-labelledby="edit"
									transform=""
									><g data-v-e9de0afc="" fill="currentColor"
										><path
											data-v-0531b344=""
											data-v-e9de0afc=""
											fill-rule="evenodd"
											clip-rule="evenodd"
											d="M5.19999 13.3L12.7 5.09996C14.5 3.09996 16.4 2.89996 18.5 4.89996C20.6 6.89996 20.4 8.89996 18.7 10.8L11.1 19C10.7 19.4 9.99999 19.8 9.39999 19.9L6.49999 20.4C4.99999 20.7 3.89999 19.6 3.99999 18.1L4.39999 15C4.39999 14.4 4.79999 13.7 5.19999 13.3ZM17.6 9.89996C18.9 8.49996 19 7.29996 17.5 5.89996C16 4.39996 15 4.59996 13.6 5.99996L6.09999 14.2C5.89999 14.4 5.69999 14.9 5.69999 15.2L5.39999 18.2C5.29999 18.9 5.69999 19.2 6.29999 19.1L9.19999 18.6C9.49999 18.6 9.89999 18.3 10.1 18.1L17.6 9.89996Z"
										/>
										<path
											data-v-0531b344=""
											data-v-e9de0afc=""
											d="M11.8 6.19992C12.2 6.09992 12.5 6.39992 12.6 6.79992C12.9 9.09992 14.7 10.7999 17 11.0999C17.4 11.0999 17.6 11.4999 17.6 11.7999C17.6 12.1999 17.2 12.3999 16.9 12.3999C14 12.0999 11.7 9.89992 11.2 6.99992C11.2 6.59992 11.4 6.29992 11.8 6.19992Z"
										/></g
									></svg
								>
							</button>

							<button
								class="btn delete-btn"
								on:click={(e) => {
									e.preventDefault();
									form_data.api_data.items.splice(i, 1);
									form_data.api_data.items = [...form_data.api_data.items];
								}}
							>
								<svg
									data-v-e9de0afc=""
									data-v-23506119=""
									data-v-f1f6c310=""
									xmlns="http://www.w3.org/2000/svg"
									viewBox="0 0 24 24"
									role="presentation"
									width="14"
									height="14"
									aria-labelledby="times"
									transform=""
									><g data-v-e9de0afc="" fill="currentColor"
										><path
											data-v-23506119=""
											data-v-e9de0afc=""
											d="M1.72,0.001c-0.696,0-1.323,0.422-1.584,1.068s-0.108,1.385,0.391,1.87l9.055,9.058l-9.055,9.058
                                c-0.447,0.429-0.627,1.066-0.471,1.666s0.624,1.068,1.224,1.224s1.236-0.024,1.666-0.471L12,14.415l9.055,9.058
                                c0.429,0.447,1.066,0.627,1.666,0.471c0.6-0.156,1.068-0.624,1.224-1.224c0.156-0.6-0.024-1.238-0.471-1.666l-9.055-9.058
                                l9.055-9.058c0.506-0.492,0.658-1.245,0.382-1.894c-0.276-0.65-0.919-1.065-1.625-1.044c-0.444,0.014-0.866,0.199-1.176,0.518
                                L12,9.576L2.945,0.52C2.623,0.187,2.181,0.001,1.72,0.001z"
										/></g
									></svg
								>
							</button>
						</div>
					</td>
				</tr>
			{/if}
		{/each}
	</tbody>

	<tfoot>
		<tr class="total-row">
			<td colspan="5" />
			<td>
				<div class="description-header" style="font-weight:bold;">סה"כ:</div>
			</td>
			<td>
				<div class="description-value" style="font-weight:bold;">
					{form_data.api_data.subtotal.toFixed(2)}
				</div>
			</td>
			<td />
		</tr>
		{#if form_data.api_data.items.length > 0 && form_data.api_data.discount}
			<tr>
				<td colspan="4" />
				<td>
					<div class="my-row">
						<label for="discount">הנחה</label>
						<select
							name="discount"
							id="discount"
							class="form-control"
							bind:value={form_data.api_data.discount.type}
						>
							<option value="amount">סכום</option>
							<option value="percentage">%</option>
						</select>
					</div>
				</td>
				<td>
					<input
						class="form-control"
						type="text"
						id="discountValue"
						name="discountValue"
						placeholder="הקלידו את ההנחה"
						bind:value={form_data.api_data.discount.value}
					/>
				</td>
				<td>
					<div class="description-value" style="font-weight:bold;">
						({form_data.api_data.discount.total})
						<!-- {#if form_data.discount.type === 'percentage'}
											{(form_data.api_data.subtotal * (form_data.discount.total / 100)).toFixed(2)}
										{:else if form_data.discount.type === 'amount'}
											{form_data.discount.total}
										{/if} -->
					</div>
				</td>
			</tr>
			<tr>
				<td colspan="5" />
				<td colspan="1">
					<div style="font-weight: bold;">מע"מ</div>
				</td>
				<td>
					<div style="font-weight: bold;">
						{form_data.api_data.tax[0].total}
					</div>
				</td>
			</tr>
			<tr>
				<td colspan="5" />
				<td colspan="2">
					<hr />
				</td>
			</tr>

			<tr>
				<td colspan="5" />
				<td colspan="1">
					<div style="font-weight: bold;">סה"כ לתשלום</div>
				</td>
				<td>
					<div
						style="font-weight: bold;
                    "
					>
						{form_data.api_data.total}
					</div>
				</td>
			</tr>
		{/if}
		<tr>
			<td colspan="6">
				<button
					class="btn btn-success mt-3"
					on:click={(e) => {
						e.preventDefault();
						add_empty_item();
					}}>הוסף פריט</button
				>
			</td>
		</tr>
	</tfoot>
</table>

<style lang="scss">
	table.document-income-table {
		width: 100%;
		border-collapse: collapse;
		border-spacing: 0;
		border: 1px solid #ddd;
		margin-bottom: 1rem;
		border-radius: 12px;
		overflow: hidden;
		thead {
			background: #f9f9f9;
			th {
				padding: 0.5rem;
				border-bottom: 1px solid #ddd;
				text-align: right;
				font-weight: bold;
				font-size: 0.9rem;
				color: #333;
				.description-header {
					font-weight: bold;
					font-size: 0.9rem;
					color: #333;
				}
			}
		}
		tbody {
			tr {
				td {
					padding: 0.5rem;
					border-bottom: 1px solid #ddd;
					text-align: right;
					font-weight: bold;
					font-size: 0.9rem;
					color: #333;
					.description-value {
						font-weight: bold;
						font-size: 0.9rem;
						color: #333;
					}
				}
			}
		}
	}

	.my-row {
		display: flex;
		flex-direction: row;
		justify-content: space-between;
		align-items: center;
		margin-left: 1rem;
		margin-right: 1rem;
	}
	.btn-success {
		background: #0dac81;
		border: 1px solid #0dac81;
		color: #fff;
		&:focus {
			outline: unset;
		}
		font-size: 1rem;
		border: inherit;
		padding-top: 0;
		padding-bottom: 0;
		border-radius: 100px;
		cursor: pointer;
		display: flex;
		justify-content: center;
		align-items: center;
		font-family: inherit;
		font-weight: 500;
		letter-spacing: 0;
		transition: all 0.5s cubic-bezier(0.075, 0.82, 0.165, 1);
		&:focus {
			outline: none;
		}
		height: 32px;
		font-size: 16px;
		line-height: 22px;
		padding: 0 20px;

		background: #0dac81;
		border: 1px solid #0dac81;
		color: #fff;

		&:hover {
			background: #0b946f;
			border: 1px solid #0b946f;
		}
		&:active {
			color: #fff;
			background: #0a8b68;
		}
		&:focus {
			color: #fff;
			border: 1px solid #0b906c;
		}
		*,
		:after,
		:before {
			box-sizing: border-box;
		}
		/*! CSS Used from: Embedded */
		::placeholder {
			color: #737376;
		}
		padding: 5px 15px;
	}
</style>
