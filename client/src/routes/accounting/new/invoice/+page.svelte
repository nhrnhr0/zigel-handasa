<script>
	import { onMount } from 'svelte';
	import { network_get_morning_info } from '$lib/network.js';
	import NewInvoiceInfo from '../../../../comonents/shered/Cards/NewInvoiceInfo.svelte';
	// get linkedDocumentIds from the url query params
	let linkedDocumentIds = [];
	let data = undefined;
	let invoice = undefined;
	let client_data = undefined;
	let title = 'חשבונית חדשה';

	onMount(async () => {
		let urlParams = new URLSearchParams(window.location.search);
		if (urlParams.has('linkedDocumentIds')) {
			linkedDocumentIds = urlParams.get('linkedDocumentIds').split(',');
		}
		let res = await network_get_morning_info(linkedDocumentIds);
		data = await res.json();

		// if all the linked documents are type=הצעת מחיר
		// itereate over the items and add them to the invoice:
		//	if there is no related_to, we copy the items from the price proposal
		//	if there is a related_to, we copy the items from the price proposal and add an item with the total of the price proposal minus the related_to invoices totals
		let all_linked_documents_are_price_proposals = true;
		for (let i = 0; i < data.docs.length; i++) {
			if (data.docs[i].type != 'הצעת מחיר') {
				all_linked_documents_are_price_proposals = false;
				break;
			}
		}

		if (all_linked_documents_are_price_proposals) {
			craete_invoice_from_price_proposals(data.docs);
		}
	});

	function craete_invoice_from_price_proposals(docs) {
		console.log('docs', docs);
		// itereate over the items and add them to the invoice:
		//	if there is no related_to, we copy the items from the price proposal
		//	if there is a related_to, we copy the items from the price proposal and add an item with the total of the price proposal minus the related_to invoices totals
		let items = [];
		let total = 0;
		let recipient = undefined;
		let total_discount = 0;
		let description = '';
		let remarks = '';
		if (docs.length == 1) {
			description = docs[0].project__names;
			remarks = 'על סמך הזמנת רכש: ' + docs[0].price_prop_order_numbers[0];
		} else {
			description = 'חשבונית מס עבור הצעת מחיר ';
			remarks = 'על סמך הזמנות רכש: ';
		}

		for (let i = 0; i < docs.length; i++) {
			let doc = docs[i];
			// TODO: hanle related_docs
			if (doc.linked_docs.length > 0) {
				console.log('doc.linked_docs', doc.linked_docs);
				items = items.concat([
					{
						description: 'יתרה מהצעת מחיר ' + doc.doc_number,
						sku: '',
						quantity: 1,
						price: parseFloat(doc.open_amount),
						currency: 'ILS',
						taxIncludedInPrice: false,
						tax: doc.api_data.tax
					}
				]);
			} else {
				items = items.concat(doc.api_data.items);
			}
			if (recipient == undefined) {
				recipient = doc.api_data.recipient;
				client_data = doc.client_data;
			}

			if (doc.api_data?.discount?.total != undefined) {
				// we add the discount only if there are no linked docs
				if (doc.linked_docs.length == 0) {
					total_discount += parseFloat(doc.api_data.discount.total);
				}
			}

			if (docs.length > 1) {
				description += doc.doc_number + ', ';
				remarks += doc.price_prop_order_numbers[0] + ', ';
			}
		}
		let discount = {};
		if (docs.length > 1) {
			description = description.substring(0, description.length - 2);
			remarks = remarks.substring(0, remarks.length - 2);
			discount = {
				type: 'amount',
				value: total_discount,
				total: total_discount
			};
		} else {
			if (docs[0].linked_docs.length == 0) {
				discount = docs[0].api_data.discount;
			}
			// discount = docs[0].api_data.discount;
		}

		// input data:
		//{ "docs": [ { "id": 29, "client__name": "ffffff", "client_morning_id": "888e2ac1-3a6f-476d-a948-0b2dfb24afb5", "project__names": "ffff2", "doc_number": "366", "type": "הצעת מחיר", "total": "58.50", "morning_id": "bc782c33-8756-4612-8069-149f6ffc81d6", "created_at": "2023-09-05T10:19:14.469798Z", "type__name": "הצעת מחיר", "api_data": { "id": "bc782c33-8756-4612-8069-149f6ffc81d6", "type": 10, "number": 366, "currency": "ILS", "date": "2023-09-04", "createdAt": 1693909140000, "subtotal": 50, "rounding": false, "tax": [ { "name": "VAT", "rate": 0.17, "total": "8.50" } ], "total": "58.50", "description": "ffff2", "remarks": "", "reverseCharge": false, "recipient": { "id": "888e2ac1-3a6f-476d-a948-0b2dfb24afb5", "name": "ffffff", "department": "", "address": "", "city": "", "zip": "", "country": "IL", "phone": "", "mobile": "", "emails": [] }, "items": [ { "description": "מוצר שמור 02", "sku": "002", "quantity": 1, "price": 15, "currency": "ILS", "taxIncludedInPrice": false, "tax": [ { "name": "VAT", "rate": 0.17 } ] }, { "description": "מוצר שמור 02", "sku": "002", "quantity": 1, "price": 15, "currency": "ILS", "taxIncludedInPrice": false, "tax": [ { "name": "VAT", "rate": 0.17 } ] }, { "description": "003 test", "sku": "", "quantity": 4, "price": 5, "currency": "ILS", "taxIncludedInPrice": false, "tax": [ { "name": "VAT", "rate": 0.17 } ] } ], "transactions": [], "files": { "signed": true, "downloadLinks": { "he": "https://sandbox.d.greeninvoice.co.il/api/v1/documents/download?d=C%2Fn46SIWxEdXGyyF71D9G6sTAFIcYT2bSEvgJHKJgt24dXVos4unWNndgc06WH96chj7QwHD6IXThTDIJFiE%2FVDIBJI%2FrunqFxkPCPjt1BRN4vVDaI7Fu0lJZu6P04nIS7OuG4kuB9Gty8%2FxMWfCac4WEtv5sFKUei%2FnteH36n%2BqP7WigzQ2W%2FHwiyOVeBFCYdjop9z%2FtD6QEkDBq28%3D", "origin": "https://sandbox.d.greeninvoice.co.il/api/v1/documents/download?d=YXuUouAY5zVvNoOGrSK0CHfasfIcn09fJQ22E8yZeDIR%2BlKVP504knU4fZbtB1chT%2F8FQvuEGE%2BLyqFPNlX4zLnMaMMxocHRe545vLOkdl40mTXz%2B1HaOTfMHeFlfWTewg8mW8aYvL33yS1PHD1iqGb598%2BYrEJDFFJ7OPl7N6P3%2F2PlJDO13tRYYFJLE2JvpObkjH2BoQg2reCbG84%3D" } }, "discount": { "type": "amount", "value": "", "total": "0.00" } }, "based_on": [], "related_to": [] }, { "id": 27, "client__name": "ffffff", "client_morning_id": "888e2ac1-3a6f-476d-a948-0b2dfb24afb5", "project__names": "heyhhhhhh", "doc_number": "364", "type": "הצעת מחיר", "total": "35.10", "morning_id": "a2efd30e-8514-4b5c-a4d6-12ec4909a02d", "created_at": "2023-09-05T09:55:52.775042Z", "type__name": "הצעת מחיר", "api_data": { "id": "a2efd30e-8514-4b5c-a4d6-12ec4909a02d", "type": 10, "number": 364, "currency": "ILS", "date": "2023-09-04", "createdAt": 1693907743000, "subtotal": 30, "rounding": false, "tax": [ { "name": "VAT", "rate": 0.17, "total": "5.10" } ], "total": "35.10", "description": "heyhhhhhh", "remarks": "hey", "reverseCharge": false, "recipient": { "id": "888e2ac1-3a6f-476d-a948-0b2dfb24afb5", "name": "ffffff", "department": "", "address": "", "city": "", "zip": "", "country": "IL", "phone": "", "mobile": "", "emails": [] }, "items": [ { "description": "מוצר שמור 02", "sku": "002", "quantity": 1, "price": 15, "currency": "ILS", "taxIncludedInPrice": false, "tax": [ { "name": "VAT", "rate": 0.17 } ] }, { "description": "מוצר שמור 02", "sku": "002", "quantity": 1, "price": 15, "currency": "ILS", "taxIncludedInPrice": false, "tax": [ { "name": "VAT", "rate": 0.17 } ] } ], "transactions": [], "files": { "signed": true, "downloadLinks": { "he": "https://sandbox.d.greeninvoice.co.il/api/v1/documents/download?d=PXpMWtGgvc5dlCJdsPTl5RtdkRZWuhR29lpWStkWw4Bm%2Bno%2B6U%2BzWxq3ARADMxM%2BW%2FmJcJ2AZRQDjTF72AjNSdfZTX4aO1GJYlZFRrkAd%2FjgO0RgmkiapW%2BlXW8at%2Bw4I%2BV23rFMOCP1YDzn%2BCYpbpmKYbBTzRuTUztXBox0bkIXGXgLRuzQRx%2FJxC%2FEL6zEX6BEpox3HUhu02Hwz7o%3D", "origin": "https://sandbox.d.greeninvoice.co.il/api/v1/documents/download?d=E7Eq%2BZMsK830Ynmi2SkP6qYk1QKKLxV3ExRHIQDuFdi2EM14R%2FHZY%2BDi8fRyQgTA9%2F5OXIvDkfKf4BqLnzBcTs4XgfItMgwHbVHTQMGmtfksxMK8hDbwvkMaPnaxNGSKfPMST%2BNOHgpJ2xYEaI4Nw1g09CD%2FgWBTu2P%2FxvPKKffB3qD8Fcye9WOEAjCdKJbtjD%2F%2BmCcQNJeaUK9EK78%3D" } }, "discount": { "type": "amount", "value": "", "total": "0.00" } }, "based_on": [], "related_to": [] } ] }

		// end result:
		// { "type": 305, "date": "2017-10-03", "vatType": 2, "lang": "en", "currency": "ILS", "description": "", "remarks": "", "footer": "lower text", "emailContent": "", "client": { "self": false, "emails": [], "id": "be79d5fb-3057-4d57-9cb8-e8bc416431ae" }, "rounding": false, "signed": true, "income": [ { "catalogNum": "d", "price": 3, "currency": "ILS", "currencyRate": 1, "quantity": 1, "description": "t", "vatType": 2, "vatRate": 0 }, { "catalogNum": "g", "price": 4, "currency": "ILS", "currencyRate": 1, "quantity": 1, "description": "t", "vatType": 2, "vatRate": 0 }, { "catalogNum": "t", "price": 50, "currency": "ILS", "currencyRate": 1, "quantity": 1, "description": "tw", "vatType": 1, "vatRate": 0.17 } ] }

		let dueDate = calculate_shotef_plus_due_date(
			new Date().toISOString().split('T')[0],
			client_data.paymentTerms
		);

		invoice = {
			type: 305,
			date: new Date().toISOString().split('T')[0],
			dueDate: dueDate,
			vatType: 0,
			lang: 'he',
			currency: 'ILS',
			footer: '',
			emailContent: '',
			client: {
				self: false,
				emails: recipient.emails,
				id: recipient.id
			},
			discount: {
				type: 'sum',
				value: total_discount,
				total: total_discount
			},
			rounding: false,
			signed: true,
			income: items,
			description: description,
			tax: docs[0].api_data.tax,
			remarks: remarks,
			linkedDocumentIds: linkedDocumentIds
		};
	}

	function calculate_shotef_plus_due_date(date, shotef) {
		if (shotef == -1) {
			return date;
		} else {
			let added_months = shotef / 30 + 1;
			let new_month_day = shotef % 30;
			let new_date = new Date(date);
			new_date.setMonth(new_date.getMonth() + added_months);
			new_date.setDate(new_month_day);
			return new_date.toISOString().split('T')[0];
		}
	}
</script>

{#if invoice}
	<NewInvoiceInfo form_data={invoice} {client_data} {title} />
{/if}
