<script>
	export let expression1 ;
	export let expression2 ;
	export let admin ;

	let DeletePromise = new Promise(()=>{});
	let UpdatePromise = new Promise(()=>{});
	let readonly=true;
	let meta;

	async function synonym(method) {
		let res;
		if (method == 'DELETE') {
			res = await fetch(`http://localhost/api/admin/synonym/${key}`,
					{method: 'DELETE'});
		} else if (method == 'PUT') {
			key = meta[0].value
			res = await fetch(`http://localhost/api/admin/synonym/${key}`, {
					method: 'PUT',
					body: JSON.stringify(meta)});
		}
		if (res.ok)  {
			return res.status
		} else {
			console.log('error')
			throw new Error('Oups');
		}
	}


function handleSubmit() {
	PutPromise = synonym('PUT')
}

</script>


<tr>
	<td><input type='text' value={expression1} {readonly}></td>
	<td><input type='text' value={expression2} {readonly}></td>
</tr>


<style>

	td input {
		border:none;
		width: 90%;
		resize: none;
		background-color: inherit;
	 }

	th, td {
  text-align: left;
  padding: 8px;
	white-space:wrap;
}

tr:nth-child(even) {background-color: #f2f2f2;}


</style>
