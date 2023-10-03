<script>
	import { onMount } from 'svelte';
	import { network_get_morning_info } from '$lib/network.js';
	import NewCancelInfo from '../../../../comonents/shered/Cards/NewCancelInfo.svelte';
	// get linkedDocumentIds from the url query params
	let linkedDocumentIds = [];
	let data = undefined;
	let form_data = undefined;
	let client_data = undefined;
	onMount(async () => {
		let urlParams = new URLSearchParams(window.location.search);
		if (urlParams.has('linkedDocumentIds')) {
			linkedDocumentIds = urlParams.get('linkedDocumentIds').split(',');
		}
		let res = await network_get_morning_info(linkedDocumentIds);
		data = await res.json();
		// 		};
		let total_discount = parseFloat(data.docs[0].api_data?.discount?.total || 0);
		client_data = data.docs[0].client_data;

		form_data = {
			type: 330,
			date: new Date().toISOString().split('T')[0],
			vatType: 0,
			lang: 'he',
			currency: 'ILS',
			footer: 'lower text', // TODO: add footer (has this code also in another part)
			emailContent: '',
			discount: {
				type: 'sum',
				value: total_discount,
				total: total_discount
			},
			client: {
				self: false,
				emails: data.docs[0].client_data.emails,
				id: data.docs[0].client_data.id
			},
			rounding: false,
			signed: true,
			tax: data.docs[0].api_data.tax,
			description: 'ביטול ' + data.docs[0].api_data?.description || '',
			income: data.docs[0].api_data.income,
			remarks: data.docs[0].remarks,
			linkedDocumentIds: linkedDocumentIds,
			subtotal: data.docs[0].api_data.subtotal,
			tax: data.docs[0].api_data.tax,
			invoice_morning_id: data.docs[0].morning_id
		};
	});
</script>

{#if data}
	<!-- hey
	{JSON.stringify(data.docs[0])} -->
	<NewCancelInfo
		title="ביטול חשבונית מס מספר {data.docs[0].doc_number}"
		{form_data}
		{client_data}
	/>
{/if}
