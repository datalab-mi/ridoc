<script>

	import { index_name, list_synonym  } from '../stores.js';

	export let expressionA ;
	export let expressionB ;

	export let admin ;

	let DeletePromise = new Promise(()=>{});
	let UpdatePromise = new Promise(()=>{});
	let readonly = true;
	let send = false;
	let meta;

	$: meta = [
						{
							key: 'expresion1',
							type: 'text',
							placeholder: 'DNUM',
							value: expressionA,
							innerHtml: 'Acronyme: '
						},
						{
							key: 'expresion2',
							type: 'text',
							placeholder: 'Direction du Numérique',
							value: expressionB,
							innerHtml: 'Signification: '
						}
					]
	async function synonym(method) {
		let res;

		res = await fetch(`http://localhost/api/admin/synonym/${expressionA}`, {
				method: method,
				body: JSON.stringify(meta)});
		$list_synonym = await res.json();

		console.log('Delete/update')
		console.log($list_synonym)
		if (res.ok)  {
			return res.status
		} else {
			console.log('error')
			throw new Error('Oups');
		}
	}


	function handleSave() {

		send = !send
		readonly = !readonly
		if (readonly & send){
			synonym('PUT')
		}
	}

function handleDelete() {
	DeletePromise = synonym('DELETE')
}

</script>

<div class="inline-flex w-full">

	<div class="flex-initial w-1/5  text-gray-700 text-center bg-gray-400 px-4 py-2 m-2">
		<input type='text' bind:value={expressionA} {readonly}>
	</div>
	<div class="flex-initial w-4/5 text-gray-700 text-center bg-gray-400 px-4 py-2 m-2">
		<input type='text' bind:value={expressionB} {readonly}>
	</div>
	<div class="flex-initial w-1/5 text-gray-700 text-center bg-gray-400 px-4 py-2 m-2">
		{#if (readonly & send) }
			<button on:click={handleSave} class="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded inline-flex items-center">
				<svg class="fill-current w-4 h-4 mr-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M12.3 3.7l4 4L4 20H0v-4L12.3 3.7zm1.4-1.4L16 0l4 4-2.3 2.3-4-4z"/></svg>
			</button>
		{:else if (!readonly & !send) }
			<button on:click={handleSave} class="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded inline-flex items-center">
				<svg class="fill-current w-4 h-4 mr-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M0 2C0 .9.9 0 2 0h14l4 4v14a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2zm5 0v6h10V2H5zm6 1h3v4h-3V3z"/></svg>

			</button>
		{:else}
			<button on:click="{() => readonly = !readonly}" class="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded inline-flex items-center">
				<svg class="fill-current w-4 h-4 mr-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M12.3 3.7l4 4L4 20H0v-4L12.3 3.7zm1.4-1.4L16 0l4 4-2.3 2.3-4-4z"/></svg>
			</button>
		{/if}
		<button on:click={handleDelete} class="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded inline-flex items-center">
			<svg class="fill-current w-4 h-4 mr-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M6 2l2-2h4l2 2h4v2H2V2h4zM3 6h14l-1 14H4L3 6zm5 2v10h1V8H8zm3 0v10h1V8h-1z"/></svg>
		</button>
	</div>

</div>



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

input {
	border:none;
	width: 90%;
	resize: none;
	background-color: inherit;
 }

</style>
