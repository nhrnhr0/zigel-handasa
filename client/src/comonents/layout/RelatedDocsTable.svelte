<script>
	import HebrewDateCell from '../list-view/cells/HebrewDateCell.svelte';
	import CurrencyCell from '../list-view/cells/currencyCell.svelte';

	export let related_docs = {};
	// {"parents":[{"id":20,"rel_total":"5000.00","doc_number":"386","type":"הצעת מחיר","total":"5000.00","doc_date":"2023-09-13 11:23:42.251336+00:00"}],"childs":[]}
	// we need to merge parents and childs into one array and sort it by doc_date desc (keep the type of each doc (parent/child))

	let merged_docs = [];

	$: {
		if (related_docs.parents && related_docs.childs) {
			let parents = related_docs.parents.map((doc) => {
				return { ...doc, parent_or_child: 'parent' };
			});
			let childs = related_docs.childs.map((doc) => {
				return { ...doc, parent_or_child: 'child' };
			});
			merged_docs = [...parents, ...childs];
			merged_docs.sort((a, b) => {
				return new Date(b.doc_date) - new Date(a.doc_date);
			});
		}
	}

	let parentTxt = 'נוצר על סמך מסמך';
	let childTxt = 'נוצר עליו מסמך';
</script>

<table>
	<thead>
		<tr>
			<th />
			<th> מספר מסמך </th>
			<th> תאריך </th>
			<th> סוג </th>
			<th> סכום </th>
		</tr>
	</thead>
	<tbody>
		{#each merged_docs as doc}
			<tr>
				<td>
					{doc.parent_or_child == 'parent' ? parentTxt : childTxt}
				</td>
				<td>{doc.doc_number}</td>
				<td>
					<HebrewDateCell data={doc.doc_date} />
				</td>
				<td>{doc.type}</td>
				<td>
					<CurrencyCell data={doc.rel_total} />
					{#if doc.rel_total != doc.total}
						(מתוך:
						<CurrencyCell data={doc.total} />)
					{/if}
				</td>
			</tr>
		{/each}
	</tbody>
</table>

<style lang="scss">
	table {
		width: 100%;
		thead {
			background-color: #f5f5f5;
			th {
				text-align: center;
				border: 1px solid #ccc;
				padding: 5px;
			}
		}
		tbody {
			tr {
				td {
					text-align: center;
					border: 1px solid #ccc;
					padding: 5px;
				}
			}
		}
	}
</style>
